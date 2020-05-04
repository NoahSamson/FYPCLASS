//=======================
// variable
//=======================
var source_name;

//========================
// Get Web page elements
//========================
// var imageFolderPath = document.getElementById("folder-path");
var preview = document.getElementById("preview");
var caption = document.getElementById("upload-caption");
var source_caption = document.getElementById("source-caption");
var source_image = document.getElementById("source-image");
var predResult = document.getElementById("show-result");

var fileSelect = document.getElementById("img-upload");

fileSelect.addEventListener("change", selectHandler, false);


function selectHandler(e) {
    var ima = document.getElementById('preview');
    var imgfilename = document.getElementById('prefilename')

    var read = new FileReader();
    read.readAsDataURL(e.target.files[0]);
    // print(e.target.files[0].name);
    read.onloadend = () => {
        console.log(e.target.files[0].name);
        // ima.src = URL.createObjectURL(e.target.files[0]);
        ima.src = read.result;
        $("#prefilename").text(e.target.files[0].name)
        $('#preview').show();
        $('#upload-caption').hide();
    }
    // source_image.src = ima.src;
    // variable couldn't change the p tag value
    // document.getElementById("source-caption").innerHTML = e.target.files[0].name;
}

//========================
//Butttons
//========================
function submit() {
    console.log('submit');
    if (!preview.src) {
        window.alert("Please select an image");
        return;
    }
    var fname = $('#prefilename').text()
    $('#submit_id').hide();
    $('#loading_id').show();
    //Call Predict Function
    predictImage(preview.src, fname);
}

// function del() {
//     console.log('delete');
// }

// Display the result from model
function displayResult() {
    var display = document.getElementById(id)
}

//========================
// Call to python Functions
//=========================
function predictImage(img, fname) {
    console.log(img)
    console.log(fname)

    var postData = {
        file_name: fname,
        image_data: img
    }

    $.ajax({
        type: "POST",
        url: "/predict_image",
        data: JSON.stringify(postData),
        contentType: "application/json",
        // dataType: "json",
        success: function (response) {
            // if (response.ok) {
            //     response.text().then(data => {
            console.log('here')
            console.log(response);

            // predResult.innerHTML += response.toString();
            // document.write(response);
            $('#res').html(response.toString());
            $('#submit_id').show();
            $('#loading_id').hide();
            // });
            // $('body').append(response);
            // }
        },
        fail: function (err) {
            $('#submit_id').show();
            $('#loading_id').hide();
            console.log(err.message);
            window.alert("Something went wrong");
        }
    });

    // fetch("/predict_image", {
    //     method: "POST",
    //     headers: {
    //         "Content-Type": "application/json"
    //     },
    //     body: JSON.stringify(img)
    // }).then(resp => {
    //     console.log(resp)
    //     if (resp.ok)
    //         resp.text().then(data => {
    //             console.log(data);
    //             document.body.innerHTML = data
    //         });
    // }).catch(err => {
    //     console.log("Error Occurred", err.message);
    //     window.alert("Something went wrong");
    // });
}


function del() {
    console.log('clear entered')
    $.ajax({
        type: "GET",
        url: "/delete_files",
        // contentType: "application/json",
        success: function (response) {
            console.log('Done');
            $('#res').html('');
            $('#preview').hide();
            $('#upload-caption').show();
        },
        fail: function (err) {
            console.log(err.message);
            window.alert("Something went wrong");
        }
    });
}


//display result
function displayResult(data) {
    predResult.innerHTML = data.label;
}

//=======================
// Utils
//=======================
function hide(l) {
    l.classList.add("hidden");
}

function show(l) {
    l.classList.remove("hidden");
}
