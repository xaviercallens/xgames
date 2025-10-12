
// Browser capability detection for Python integration
function detectBrowserCapabilities() {
    const capabilities = {
        wasm_support: typeof WebAssembly !== 'undefined',
        memory_mb: navigator.deviceMemory ? navigator.deviceMemory * 1024 : 512,
        cpu_cores: navigator.hardwareConcurrency || 2,
        is_mobile: /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent),
        connection_speed: navigator.connection ? navigator.connection.effectiveType : 'good',
        screen_width: window.screen.width,
        screen_height: window.screen.height,
    };
    
    // Send to Python via custom event or API
    window.browserCapabilities = capabilities;
    
    return capabilities;
}

// Auto-detect on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', detectBrowserCapabilities);
} else {
    detectBrowserCapabilities();
}

// Expose globally
window.detectBrowserCapabilities = detectBrowserCapabilities;
