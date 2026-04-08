const collect = () => {
    const info = {
        res: window.screen.width + "x" + window.screen.height,
        mem: navigator.deviceMemory,
        cores: navigator.hardwareConcurrency,
        ua: navigator.userAgent
    };
    console.log("Telemetry found:", info);
};
collect();