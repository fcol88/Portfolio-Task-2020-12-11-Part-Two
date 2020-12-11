document.getElementById('description').onkeyup = function() {
    const charLimit = 500;
    var chars = this.value.length;
    var charsRemaining = charLimit - chars;

    if(charsRemaining <= 0) {
        this.value = this.value.substring(0, 500);
        charsRemaining = 0;
    }

    document.getElementById('remaining').innerHTML = charsRemaining;
}