var total_photos_counter = 0;
var mycount = 0;
Dropzone.options.myDropzone = {
    uploadMultiple: true,
    parallelUploads: 5,
    paramName:"file",
    maxFilesize: 5,
    previewTemplate: document.querySelector('#preview').innerHTML,
    acceptedFiles: '.jpg, .jpeg, .png',
    addRemoveLinks: false,
    dictRemoveFile: 'Remove file',
    dictFileTooBig: 'Image size should not be greater than 5MB',
    timeout: 180000,
 
    init: function () {

        this.on("maxfilesexceeded", function(file){
            var error_message = "<h4 class='error-upload-limit-message-div'>Maximum files upload limit reached.</h4>";
            $('.error-upload-limit-message-div').replaceWith(error_message);
        });

        this.on("error", function(file, message,response) {
            // mycount--;
            mycount = 0;
            total_photos_counter--;
            $("#dropzoneImageCounter").text(mycount); 
            
            var error_message = "<h4 class='error-message-div'>"+file.name+" :- "+message+".</h4>";
            this.removeFile(file);
                
            if($('.error-message-div').text().length > 0){
                // console.log('inside loop');
                var append_error_message = "<br>"+file.name+" :- "+message+".";
                $('.error-message-div').append(append_error_message);
            }else{
                $('.error-message-div').replaceWith(error_message);
            }
            // console.log('error end');
        });
        $.get('/administrator/product/multiple-images/server-images/'+id, function(data) {
            var string_list_images = "";
            $.each(data.images, function (key, value) {
                var file = {id:value.id,name: value.imageName, size: value.size};
                // console.log(value);
                if(value.labelName != null){
                    file['label']=value.labelName;
                }else{
                    file['label']='';
                }
                // console.log(file);
                total_photos_counter++;
                string_list_images += "<div class='sl-sl_preview sl-sl_processing sl-sl_image-sl_preview'> <div class='sl-sl_image'><img alt='"+file.name+"' src='/uploads/product/multiple_images/"+file.name+"' height='120' width='120'></div><div class='sl-sl_details'><div class='sl-sl_filename'><span>"+file.name+"</span></div></div><div class='sl_label_div'><input type='text' value='"+file.label+"' class='sl_remove unlink_label' placeholder='Label name' name='label_name_"+file.id+"' id='label_name_"+file.id+"'></div><div class='sl_checkbox_div'><input type='checkbox' class='sl_remove unlink_checkbox' value='"+file.id+"' id='image_id_"+file.id+"' name='image_name_"+file.id+"'></div></div>";
                
            });
            $("#existing_images").html(string_list_images);
            $("#exisitingImageCounter").text(total_photos_counter);
        });
    },
    
    processing: function(file,message){
        mycount++;
        $("#dropzoneImageCounter").text(mycount);
        // console.log('process end');
    },
    success: function (file, response) {
        mycount--;
        $("#dropzoneImageCounter").text(mycount);
        
        var success_string_list_images = "<div id='existing_images' class='separate_list'>";
        count = response.images.length;
        $.each(response.images, function (key, value) {
            var file = {id:value.id,name: value.imageName, size: value.size};
            if(value.labelName != null){
                file['label']=value.labelName;
            }else{
                file['label']='';
            }
            success_string_list_images += "<div class='sl-sl_preview sl-sl_processing sl-sl_image-sl_preview'> <div class='sl-sl_image'><img alt='"+file.name+"' src='/uploads/product/multiple_images/"+file.name+"' height='120' width='120'></div><div class='sl-sl_details'><div class='sl-sl_filename'><span>"+file.name+"</span></div></div><div class='sl_label_div'><input type='text' class='sl_remove unlink_label' value='"+file.label+"' placeholder='Label name' name='label_name_"+file.id+"' id='label_name_"+file.id+"'></div><div class='sl_checkbox_div'><input type='checkbox' class='sl_remove unlink_checkbox' value='"+file.id+"' id='image_id_"+file.id+"' name='image_name_"+file.id+"'></div></div>";
            // console.log('test');
        });
        success_string_list_images +="</div>";
        var uploaded_count_string= "<span id='exisitingImageCounter'>"+count+"</span>";
        var uploading_count_string= "<span id='dropzoneImageCounter'>"+total_photos_counter+"</span>";
        // console.log(success_count_string);
        $("#existing_images").replaceWith(success_string_list_images);
        $("#exisitingImageCounter").replaceWith(uploaded_count_string);
        
        this.removeFile(file);
    },
    error: function(file,response) {
        return false;
    },
};