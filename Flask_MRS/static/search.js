

var list = document.getElementById('list')
var input = document.getElementsByName('name')[0];
var btn = document.getElementsByName('btn')[0];
btn.addEventListener('click', function () {
    const value = input.value;
    console.log(value);
    if (value && value.trim().length > 0 ){
        getMovies(value);
    } else {
        clearList()
    }

});

function getMovies(name) {
    fetch("https://imdb-internet-movie-database-unofficial.p.rapidapi.com/search/"+name, {
    "method": "GET",
    "headers": {
    	"x-rapidapi-host": "imdb-internet-movie-database-unofficial.p.rapidapi.com",
    	"x-rapidapi-key": "ae2f772566msh53a562e84ed2f81p1d96fajsne0717a4d8a5d"
    }
    })
    .then(res => res.json())
    .then( data => {
        if(data.message)
            setNoResults()
        else {
            addlist(data.titles)
        }
    })
    .catch(err => { setNoResults(); })

    
    }
function addlist(group) {
    clearList();
    for(const movie of group){
        const item=document.createElement('li');
        item.classList.add('list-group-item');
        const img = document.createElement('img');
        img.classList.add('img-thumbnail mr-2');
        img.src=movie.image;
        item.appendChild(img);
        const text= document.createTextNode(movie.title);
        item.appendChild(text);
        const btn = document.createElement('a');
        btn.classList.add('btn btn-outline-dark btn-sm float-center')
        const Add = document.createTextNode('Add');
        btn.appendChild(Add);
        item.appendChild(btn);
        list.appendChild(item);
    }
    if(group.length===0) setNoResults()
}
function clearList() {
    while (list.firstChild) {
        list.removeChild(list.firstChild);
    }
}
function setNoResults() {
    clearList()
    const item=document.createElement('li');
        item.classList.add('list-group-item');
        const text= document.createTextNode('No results found');
        item.appendChild(text);
        list.appendChild(item);
}

