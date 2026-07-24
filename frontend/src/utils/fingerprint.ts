// Client Hardware Fingerprint Generator for EVU NEXA AI
export async function getHardwareFingerprint(): Promise<string> {
  const components: string[] = [];

  // 1. User Agent & System Info
  components.push(navigator.userAgent);
  components.push(navigator.language);
  components.push(String(navigator.hardwareConcurrency || 4));
  components.push(String(screen.width) + 'x' + String(screen.height));
  components.push(String(screen.colorDepth));

  // 2. Canvas 2D Render Signature
  try {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    if (ctx) {
      canvas.width = 200;
      canvas.height = 50;
      ctx.textBaseline = 'top';
      ctx.font = '14px "Arial"';
      ctx.textBaseline = 'alphabetic';
      ctx.fillStyle = '#f60';
      ctx.fillRect(125, 1, 62, 20);
      ctx.fillStyle = '#069';
      ctx.fillText('EVU-NEXA-AI-FP-2026', 2, 15);
      ctx.fillStyle = 'rgba(102, 204, 0, 0.7)';
      ctx.fillText('EVU-NEXA-AI-FP-2026', 4, 17);
      components.push(canvas.toDataURL());
    }
  } catch (e) {
    components.push('canvas-error');
  }

  // 3. Crypto Hash SHA-256
  const rawString = components.join('###');
  const msgUint8 = new TextEncoder().encode(rawString);
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgUint8);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');

  return hashHex;
}
