$(document).ready( function() {

    console.log("init")
    
    $("#bulkUploadButton").on("click", function() {
        
        $(".visually-hidden").removeClass("visually-hidden")
        console.log("tried removing class")
    })
})