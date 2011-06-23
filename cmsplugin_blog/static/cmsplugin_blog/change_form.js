(function($) {
    $(document).ready(function() {
        // saveform event handler
        $('#entry_form').submit(function(){
            if($('iframe').length){
                var question = gettext("Not all plugins are saved. Are you sure you want to save the page?\nAll unsaved plugin content will tried to save.");
                var answer = confirm(question, true);
                if (answer){
                    $('iframe').contents().find('#content-main>form').each(function(){
                        try{
                            this.submit();
                        } catch(err) { 
                            return false;
                        }
                    });
                    return true;
                }else{
                    return false;
                }
            }
        });
    });
})(blog.jQuery);
