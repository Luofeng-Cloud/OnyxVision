// OnyxVision Frontend API Client
// Handles real HTTP communication with backend FastAPI endpoints

export async function fetchHomeMedia(sourceId = null) {
  try {
    const url = sourceId ? ('/api/media/home?source_id=' + encodeURIComponent(sourceId)) : '/api/media/home';
    const res = await fetch(url);
    if (!res.ok) throw new Error('HTTP ' + res.status + ': ' + res.statusText);
    return await res.json();
  } catch (err) {
    console.warn('[API] fetchHomeMedia error, falling back to offline store:', err);
    return null;
  }
}

export async function fetchSources() {
  try {
    const res = await fetch('/api/sources');
    if (!res.ok) throw new Error('HTTP ' + res.status + ': ' + res.statusText);
    const data = await res.json();
    return data.sources || [];
  } catch (err) {
    console.warn('[API] fetchSources error:', err);
    return null;
  }
}

export async function connectEmby(payload) {
  try {
    const res = await fetch('/api/emby/connect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) {
      let errorMsg = 'HTTP ' + res.status;
      try {
        const contentType = res.headers.get('content-type') || '';
        if (contentType.includes('application/json')) {
          const errData = await res.json();
          errorMsg = errData.detail || errorMsg;
        } else {
          const text = await res.text();
          if (text) errorMsg = text.substring(0, 80);
        }
      } catch {
        // Safe fallback
      }
      throw new Error(errorMsg);
    }
    return await res.json();
  } catch (err) {
    console.error('[API] connectEmby error:', err);
    throw err;
  }
}

export async function syncEmby(sourceId) {
  try {
    const res = await fetch('/api/emby/sync', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ source_id: sourceId })
    });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    return await res.json();
  } catch (err) {
    console.warn('[API] syncEmby error:', err);
    throw err;
  }
}

export async function reportPlaybackProgress(payload) {
  try {
    await fetch('/api/playback/progress', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  } catch (err) {
    // Silent fail for heartbeats
  }
}

export async function fetchPlaybackHistory() {
  try {
    const res = await fetch('/api/playback/history');
    if (!res.ok) throw new Error('HTTP ' + res.status);
    return await res.json();
  } catch (err) {
    return null;
  }
}