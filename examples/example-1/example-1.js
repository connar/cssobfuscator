(async () => {
    const data = "EXAMPLE_OF_DATA_WE_WANT_TO_HIDE";
    const blob = "TEST:" + btoa(data);
    await navigator.clipboard.writeText(blob);
    console.log("Data copied to clipboard.");
})();