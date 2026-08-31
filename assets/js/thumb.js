// document.addEventListener('DOMContentLoaded', function() {
//     const input = document.getElementById('01');
//     if (!input) return;

//     input.addEventListener('change', function(e) {
//         const preview = document.getElementById('preview');
//         preview.innerHTML = '';

//         const files = Array.from(e.target.files);

//         if (files.length > 5) {
//             alert("最大5枚までアップロードできます。");
//             input.value = '';  // 入力をクリア
//             return;
//         }

//         files.forEach(file => {
//             if (file.type.startsWith('image/')) {
//                 const img = document.createElement('img');
//                 img.classList.add("preview-img");
//                 img.src = URL.createObjectURL(file);
//                 preview.appendChild(img);
//             }
//         });
//     });
// });
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('01');
    if (!input) return;

    input.addEventListener('change', function(e) {

        console.log("FILES:", e.target.files);
        console.log("FILE COUNT:", e.target.files.length);

        for (const file of e.target.files) {
            console.log(
                "FILE:",
                file.name,
                file.type,
                file.size
            );
        }

        const preview = document.getElementById('preview');
        preview.innerHTML = '';

        const files = Array.from(e.target.files);

        if (files.length > 5) {
            alert("最大5枚までアップロードできます。");
            input.value = '';
            return;
        }

        files.forEach(file => {
            if (file.type.startsWith('image/')) {
                const img = document.createElement('img');
                img.classList.add("preview-img");
                img.src = URL.createObjectURL(file);
                preview.appendChild(img);
            }
        });
    });
});