-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here

local notes_dir = vim.fn.expand("~/Documents/ObsidianVault")

local function notes_available()
  return (vim.uv or vim.loop).fs_stat(notes_dir) ~= nil
end

local function notify_missing_notes()
  vim.notify("Notes vault not found: " .. notes_dir, vim.log.levels.WARN)
end

local function snacks_picker(name, opts)
  local snacks = rawget(_G, "Snacks") or require("snacks")
  snacks.picker[name](opts)
end

vim.keymap.set("n", "<leader>Nf", function()
  if not notes_available() then
    return notify_missing_notes()
  end
  snacks_picker("files", { cwd = notes_dir })
end, { desc = "Find notes" })

vim.keymap.set("n", "<leader>Ng", function()
  if not notes_available() then
    return notify_missing_notes()
  end
  snacks_picker("grep", { cwd = notes_dir })
end, { desc = "Grep notes" })

vim.keymap.set("n", "<leader>Nd", function()
  if not notes_available() then
    return notify_missing_notes()
  end
  local daily_dir = vim.fs.joinpath(notes_dir, "daily")
  vim.fn.mkdir(daily_dir, "p")
  local note = vim.fs.joinpath(daily_dir, os.date("%Y-%m-%d") .. ".md")
  vim.cmd("edit " .. vim.fn.fnameescape(note))
end, { desc = "Daily note" })
