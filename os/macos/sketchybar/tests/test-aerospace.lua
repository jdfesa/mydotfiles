-- Pruebas con callbacks diferidos: no requieren Sketchybar ni AeroSpace reales.
local module_dir = assert(arg[0]:match("^(.*)/tests/[^/]+$"))
local module_path = module_dir .. "/items/spaces/window_managers/aerospace.lua"
local original_popen = io.popen
io.popen = function()
  error("La inicialización no debe usar io.popen")
end

local function fixture(with_front_app)
  local items, requests, commands = {}, {}, {}
  local anonymous = 0
  package.loaded["helpers.spaces_util.app_icons"] = { default = "?" }
  SPACES = { ITEM_PADDING = 4 }
  COLORS = { mauve = 1, text = 2, subtext0 = 3, lavender = 4, base = 5, surface1 = 6, red = 7 }
  GROUP_PADDINGS = 2
  SBAR = {
    add = function(kind, name, config)
      assert(kind == "item")
      if type(name) == "table" then
        config = name
        anonymous = anonymous + 1
        name = "anonymous." .. anonymous
      end
      assert(not items[name], "Ítem duplicado: " .. name)
      local item = { config = config }
      function item:subscribe(event, callback) self[event] = callback end
      function item:set(value) self.last_set = value end
      items[name] = item
      return item
    end,
    exec = function(command, callback)
      table.insert(commands, command)
      if command:find("list%-workspaces") then
        assert(command:match("%-%-json$"), "Usar JSON para conservar los IDs como strings")
        table.insert(requests, { command = command, callback = callback })
      elseif callback then
        callback("", 0)
      end
    end,
    remove = function(name)
      assert(items[name], "Se intentó eliminar dos veces: " .. name)
      items[name] = nil
    end,
    query = function(name)
      assert(name == "bar")
      local names = {}
      for item_name in pairs(items) do table.insert(names, item_name) end
      return { items = names }
    end,
    animate = function(_, _, callback) callback() end,
  }
  local manager = dofile(module_path)
  manager:init()
  manager:start_watcher()
  if with_front_app ~= false then
    SBAR.add("item", "front_app", {})
  end
  assert(items.aerospace_mode, "El indicador de modo no debe esperar al proceso externo")
  assert(not items["space.1"], "La carga inicial debe devolver antes del callback")
  local retry = items.aerospace_retry.routine
  local function respond(data, exit_code)
    local request = assert(table.remove(requests, 1), "Falta consulta pendiente")
    request.callback(data, exit_code)
    return request.command
  end
  local function complete(names, focused)
    local rows = {}
    for _, name in ipairs(names) do table.insert(rows, { workspace = name }) end
    assert(respond(rows, 0):match("%-%-all"))
    assert(respond({ { workspace = focused } }, 0):match("%-%-focused"))
    assert(not items.aerospace_retry, "Eliminar el timer al completar la inicialización")
    local last_item = "space." .. names[#names]
    local quoted_item = "'" .. last_item:gsub("'", "'\\''") .. "'"
    local expected_move = "/usr/local/bin/sketchybar --move front_app after " .. quoted_item
    local found_move = false
    for _, command in ipairs(commands) do
      if command == expected_move then found_move = true end
    end
    assert(found_move == (with_front_app ~= false), "Posicionar la app activa tras el último workspace")
    for _, name in ipairs(names) do
      local item = assert(items["space." .. name])
      assert(item.config.icon.string == name)
      assert(item.config.icon.highlight == (name == focused))
      item["mouse.clicked"]({ BUTTON = "left" })
      assert(commands[#commands] == "/usr/local/bin/aerospace workspace " .. name)
    end
    local count = 0
    for name in pairs(items) do if name:match("^space%.") then count = count + 1 end end
    assert(count == #names)
    retry() -- Un evento ya encolado no debe recrear los ítems.
    assert(#requests == 0)
  end
  return { items = items, requests = requests, retry = retry, respond = respond, complete = complete }
end

local numeric = { "1", "2", "3", "4", "5" }
local tests = {
  { "ready numeric process", function()
    local f = fixture()
    f.retry()
    f.retry()
    assert(#f.requests == 1, "No solapar consultas pendientes")
    f.complete(numeric, "3")
  end },
  { "legacy process", function()
    fixture().complete({ "U", "I", "O", "P", "Y", "N" }, "I")
  end },
  { "front app disabled", function()
    fixture(false).complete(numeric, "1")
  end },
  { "workspace names are shell quoted", function()
    fixture().complete({ "1", "with'quote" }, "1")
  end },
  { "failed workspace query", function()
    local f = fixture()
    f.respond({}, 1)
    assert(f.items.aerospace_retry)
    f.retry()
    f.complete(numeric, "2")
  end },
  { "empty and invalid responses", function()
    local f = fixture()
    f.respond("not JSON", 0)
    f.retry()
    f.respond({ {}, { workspace = 1 }, { workspace = "" } }, 0)
    f.retry()
    f.complete(numeric, "1")
  end },
  { "focused query failure", function()
    local f = fixture()
    f.respond({ { workspace = "1" } }, 0)
    f.respond({}, 1)
    f.retry()
    f.complete(numeric, "4")
  end },
  { "bounded retries", function()
    local f = fixture()
    f.respond({}, 1)
    for _ = 1, 10 do
      f.retry()
      f.respond({}, 1)
    end
    assert(not f.items.aerospace_retry)
    assert(not f.items["space.1"])
    assert(f.items.aerospace_mode)
  end },
}
for _, test in ipairs(tests) do
  test[2]()
  print("OK: " .. test[1])
end
io.popen = original_popen
print(#tests .. " isolated asynchronous AeroSpace initialization tests passed.")
