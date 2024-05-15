$(document).ready(function() {
    const storyContainer = $('#story-container');
    let lastTimestamp = null;

    function formatTime(timestamp) {
        const hours = timestamp.getHours().toString().padStart(2, '0');
        const minutes = timestamp.getMinutes().toString().padStart(2, '0');
        const seconds = timestamp.getSeconds().toString().padStart(2, '0');
        return `${hours}:${minutes}:${seconds}`; // Formatieren der Uhrzeit (HH:MM:SS)
    }

    function fetchAndAppendNewPhrases() {
        $.ajax({
            url: 'http://localhost:8000/story',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                const newPhrases = data.filter(obj => obj.timestamp > lastTimestamp);
                newPhrases.forEach(obj => {
                    const timestamp = new Date();
                    if (!isNaN(timestamp.getTime())) {
                        const timeDiv = $('<div></div>').addClass('time').text(formatTime(timestamp));
                        const phraseDiv = $('<div></div>').addClass('phrase').text(obj.storyphrase);
                        const div = $('<div></div>').addClass('story-phrase').append(timeDiv, phraseDiv);
                        div.attr('id', obj.timestamp);
                        storyContainer.prepend(div);
                    } else {
                        console.error('Invalid timestamp:', obj.timestamp);
                    }
                });
                if (newPhrases.length > 0) {
                    lastTimestamp = newPhrases[newPhrases.length - 1].timestamp;
                }
            },
            error: function(xhr, status, error) {
                console.error('Error fetching story:', error);
            }
        });
    }

    fetchAndAppendNewPhrases(); // Fetch and append initial phrases

    setInterval(fetchAndAppendNewPhrases, 500); // Fetch and append every 30 seconds
});
