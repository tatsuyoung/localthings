// wanakana.jsを使って日本語をローマ字に変換する関数を定義
console.log("wanakana:", typeof wanakana);

var titleInput = document.querySelector('input[name=title]');
var slugInput = document.querySelector('input[name=slug]');

var slugify = (val) => {
    return val.toString().toLowerCase().trim()
    .replace(/&/g, '-and-')
    .replace(/[\s\W-]+/g, '-')
    };
titleInput.addEventListener('keyup', (e) => {
    slugInput.setAttribute('value', slugify(titleInput.value));
});
