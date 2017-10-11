(function () {
    function loadJSON(url, callback) {
        var request = new XMLHttpRequest();
        request.overrideMimeType('application/json');
        request.open('GET', url, true);
        request.onreadystatechange = function () {
            if (request.readyState === 4 && request.status === 200) {
                callback(request.responseText)
            }
        };
        request.send(null)
    }

    var backlinksDiv = document.querySelector('#backlinks');

    var type = backlinksDiv.getAttribute('type');
    var parameter = backlinksDiv.getAttribute('data-backlinks');

    loadJSON('/api/backlinks/' + type + '/' + parameter, function (response) {
        var types = {};
        var jsonAnswer = JSON.parse(response);
        if (jsonAnswer.length > 0) {
            // console.log(jsonAnswer);
            var h = document.createElement('h5');
            h.appendChild(document.createTextNode('Recipe used by:'));
            backlinksDiv.appendChild(h);
            var ul = document.createElement('ul');
            jsonAnswer.forEach(function (elem) {
                var li = document.createElement('li');
                var anker = document.createElement('a');
                anker.setAttribute('href', '../' + elem['path']);
                var typeText = '';
                if (elem['path'].match(/^(experiment\/).*/)) {
                    typeText = ' (Experiment)';
                } else if (elem['path'].match(/^(dataset\/).*/)) {
                    typeText = ' (Dataset)';
                }
                anker.appendChild(document.createTextNode(elem['name'] + ' - ' + elem['version']));
                li.appendChild(anker);
                li.appendChild(document.createTextNode(typeText));
                ul.appendChild(li);
            });
            backlinksDiv.appendChild(ul);
        }
    })
})();