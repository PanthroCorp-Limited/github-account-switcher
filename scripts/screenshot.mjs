import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import { dirname, join, resolve } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const htmlFile = resolve(__dirname, 'mockup.html');
const outDir = resolve(__dirname, '..', 'docs', 'screenshots');

const browser = await chromium.launch();
const page = await browser.newPage();

await page.setViewportSize({ width: 420, height: 380 });
await page.goto(`file://${htmlFile}`);

// Wait for fonts and layout to settle
await page.waitForTimeout(500);

// Full scene: panel + open menu
await page.screenshot({
  path: join(outDir, 'tray-menu.png'),
  clip: { x: 0, y: 0, width: 420, height: 340 },
});
console.log('Saved tray-menu.png');

// Close-up of just the tray icon in the panel
await page.screenshot({
  path: join(outDir, 'tray-icon.png'),
  clip: { x: 332, y: 4, width: 80, height: 34 },
});
console.log('Saved tray-icon.png');

await browser.close();
console.log('Done.');
