function ui_single_update_active(element, active)
{
      element.find('div.progress').toggleClass('d-none', !active);
      element.find('input[type="text"]').toggleClass('d-none', active);

      element.find('input[type="file"]').prop('disabled', active);
      element.find('.btn').toggleClass('disabled', active);

      element.find('.btn span').toggleClass('spinner-border spinner-border-sm', active);
      // element.find('.btn i').toggleClass('fa-folder-o', !active);
}

function ui_single_update_progress(element, percent, active)
{
    active = (typeof active === 'undefined' ? true : active);

    var bar = element.find('div.progress-bar');

    bar.width(percent + '%').attr('aria-valuenow', percent);
    bar.toggleClass('progress-bar-striped progress-bar-animated', active);

    if (percent === 0){
        bar.html('');
    } else {
        bar.html(percent + '%');
    }
}

function ui_single_update_status(element, message, color)
{
    color = (typeof color === 'undefined' ? 'muted' : color);

    element.find('small.status').prop('class','status text-' + color).html(message);
}

$(document).ready(function () {
    $("#drag-and-drop-zone").dmUploader({
        multiple: false,
        url: '/products/upload/',
        fieldName: 'products_file',

        onInit: function(){
            console.log('Callback: Plugin initialized');
        },
        onDragEnter: function(){
          // Happens when dragging something over the DnD area
          this.addClass('active');
        },
        onDragLeave: function(){
            // Happens when dragging something OUT of the DnD area
            this.removeClass('active');
        },
        onBeforeUpload: function(id){
            // about tho start uploading a file
            ui_single_update_progress(this, 0, true);
            ui_single_update_active(this, true);
            ui_single_update_status(this, 'Uploading...');
        },
        onUploadProgress: function(id, percent){
            // Updating file progress
            ui_single_update_progress(this, percent);
        },
        onUploadError: function(id, xhr, status, message){
            // Happens when an upload error happens
            ui_single_update_active(this, false);
            if (xhr.responseJSON){
                if (xhr.responseJSON.products_file) {
                    message = xhr.responseJSON.products_file[0];
                }  else {
                    message = xhr.responseJSON.non_field_errors[0];
                }
            }
            ui_single_update_status(
                this, 'Error: ' + message, 'danger');
        },
        onUploadSuccess: function(id, data){
            ui_single_update_status(this, 'Importing Products ...');
            $("#import-logs-1").toggleClass('invisible');
        },
        onFileExtError: function(file){
            ui_single_update_status(
                this, 'File extension not allowed', 'danger');
        }
    });

    const es = new ReconnectingEventSource(
        'https://8278d577.fanoutcdn.com/import-events/');

    es.addEventListener('message', function (e) {
        const j_data = JSON.parse(e.data);
        const current_date = new Date();
        const datetime = current_date.getDate() + "/"
                + (current_date.getMonth()+1)  + "/"
                + current_date.getFullYear() + " @ "
                + current_date.getHours() + ":"
                + current_date.getMinutes() + ":"
                + current_date.getSeconds();
        $("#import-logs-2 ul").prepend(
            "<li>"+ datetime + ": " + j_data['log'] +"</li>");
    }, false);
    es.addEventListener('end', function (e) {
        location.reload()
    }, false);

    // Check for current uploads
    if ($("#id_current_upload").attr('value')){
        $("#import-logs-1").toggleClass('invisible');
        const d_zone = $("#drag-and-drop-zone");
        ui_single_update_progress(d_zone, 100);
        ui_single_update_active(d_zone, true);
        ui_single_update_status(d_zone, 'Importing...');
    }
});
