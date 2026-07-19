const { app, BrowserWindow, ipcMain, shell } = require('electron');
const path = require('path');
const os = require('os');

let mainWindow;
let httpServer = null;
const serverPath = path.join(__dirname, '..', 'server.js');

function getLocalIP() {
  const interfaces = os.networkInterfaces();
  for (const name of Object.keys(interfaces)) {
    for (const iface of interfaces[name]) {
      if (iface.family === 'IPv4' && !iface.internal) {
        return iface.address;
      }
    }
  }
  return 'localhost';
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 480, height: 520,
    resizable: false,
    webPreferences: { nodeIntegration: true, contextIsolation: false },
    title: '매크로실습실',
  });
  mainWindow.loadFile(path.join(__dirname, 'ui.html'));
  mainWindow.setMenuBarVisibility(false);
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (httpServer) {
    if (httpServer.closeAllConnections) httpServer.closeAllConnections();
    httpServer.close();
  }
  app.quit();
});

ipcMain.handle('start-server', async () => {
  try {
    const { startServer } = require(serverPath);
    httpServer = await startServer();
    const ip = getLocalIP();
    return { success: true, ip };
  } catch (e) {
    return { success: false, error: e.message };
  }
});

ipcMain.handle('stop-server', async () => {
  if (httpServer) {
    if (httpServer.closeAllConnections) httpServer.closeAllConnections();
    await new Promise(resolve => {
      httpServer.close(resolve);
      setTimeout(resolve, 3000);
    });
    httpServer = null;
    const resolvedPath = require.resolve(serverPath);
    delete require.cache[resolvedPath];
  }
  return { success: true };
});

ipcMain.on('open-browser', (e, ip) => shell.openExternal(`http://${ip}:3000`));
ipcMain.on('open-admin', (e, ip) => shell.openExternal(`http://${ip}:3000/admin.html`));
