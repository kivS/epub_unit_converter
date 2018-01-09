<script>
  export default{
    name: 'file-uploader',
    props: [
        'epubs'
    ],
    methods:{
        handle_on_drop: function(e){
            // datatranfer object
            const dt = e.dataTransfer

            let file = null

            // check which interface has file
            if(dt.items && dt.items.length > 0){
                for (var i = 0; i < dt.items.length; i++) {
                    file = dt.items[i].getAsFile()
                    this.processFile(file)
                }
            }else{
                for (var i = 0; i < dt.files.length; i++) {
                    file = dt.files[i]
                    this.processFile(file)
                }
            }

        },
        handle_on_drag_end: function(e){
            // clean files from dataTransfer object
            let dt = ev.dataTransfer

            if(dt.items && dt.items.length > 0){
                for (var i = 0; i < dt.items.length; i++) {
                    dt.items.remove(i)
                }
            }else{
                dt.clearData()
            }
        },
        handle_click: function(e){
            // emit click event on file input
            this.$refs.file_input.click()
        },
        handle_file_input_change: function(e){
            console.log('input change event:', e)
            let files = e.target.files

            for (var i = 0; i < files.length; i++) {
                this.processFile(files[i])
            }

            // reset input value 
            e.target.value = null
        },

        processFile: function(file){
            console.log('Processing file:', file)

            if(file.type != 'application/epub+zip'){
                TOAST.error({
                    message: `${file.name} is not supported. Epub files only.`
                })
                return
            }

            // load contents of file
            let f = new FileReader()
            f.readAsDataURL(file)
            f.onerror = e =>{
                console.error(e)
            }
            f.onload = e =>{
                // create epub object
                const epub = {
                    name: file.name,
                    bin_data: e.target.result
                }

                /*console.log('epub data:',epub)
                return*/

                // send epub for further processing
                BUS.$emit('add_epub_file', epub)
            }
        },

        download_epub: function(name){
          console.log('downloading:', name);
          location.replace(`http://localhost:7000/download_epub/${name}`)
        },

        handle_delete_epub: function(name){
            BUS.$emit('remove_epub', name)
        }
    }
  }  
</script>

<template>
    <div class="dropzone_area" v-on:dragover.prevent @drop.prevent="handle_on_drop" @dragend="handle_on_drag_end">
        <!-- ghost file input  -->
        <input type="file" ref="file_input" multiple accept="application/epub+zip" style="display:none" @change="handle_file_input_change">
        <p class="dropzone_text_hint" @click="handle_click">Click here or drag files to upload</p>
        <div class="epub_list">
            <div class="epub" v-for="(epub,epub_name,index) in epubs" :key="index">
                <!-- show conversion button -->
                <svg @click="$modal.show('conversions', epub_name)" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="btns show_conversions">
                    <line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line>
                    <line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3" y2="6"></line>
                    <line x1="3" y1="12" x2="3" y2="12"></line><line x1="3" y1="18" x2="3" y2="18"></line>
                </svg>
                
                <!-- delete button -->
                <svg @click="handle_delete_epub(epub_name)"  xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="btns delete">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="15" y1="9" x2="9" y2="15"></line>
                    <line x1="9" y1="9" x2="15" y2="15"></line>
                </svg>

                <span class="title">{{ epub_name }}</span>

                <!-- Download button -->
                <svg v-if="epub.ready"  @click="download_epub(epub_name)" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="btns download">
                    <polyline points="8 17 12 21 16 17"></polyline>
                    <line x1="12" y1="12" x2="12" y2="21"></line>
                    <path d="M20.88 18.09A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.29"></path>
                </svg>

                <!-- Loading -->
                <svg v-else width="45" height="45" viewBox="0 0 45 45" xmlns="http://www.w3.org/2000/svg" stroke="#00bcd4" class="loader">
                    <g fill="none" fill-rule="evenodd" transform="translate(1 1)" stroke-width="2">
                        <circle cx="22" cy="22" r="6" stroke-opacity="0">
                            <animate attributeName="r"
                                 begin="1.5s" dur="3s"
                                 values="6;22"
                                 calcMode="linear"
                                 repeatCount="indefinite" />
                            <animate attributeName="stroke-opacity"
                                 begin="1.5s" dur="3s"
                                 values="1;0" calcMode="linear"
                                 repeatCount="indefinite" />
                            <animate attributeName="stroke-width"
                                 begin="1.5s" dur="3s"
                                 values="2;0" calcMode="linear"
                                 repeatCount="indefinite" />
                        </circle>
                        <circle cx="22" cy="22" r="6" stroke-opacity="0">
                            <animate attributeName="r"
                                 begin="3s" dur="3s"
                                 values="6;22"
                                 calcMode="linear"
                                 repeatCount="indefinite" />
                            <animate attributeName="stroke-opacity"
                                 begin="3s" dur="3s"
                                 values="1;0" calcMode="linear"
                                 repeatCount="indefinite" />
                            <animate attributeName="stroke-width"
                                 begin="3s" dur="3s"
                                 values="2;0" calcMode="linear"
                                 repeatCount="indefinite" />
                        </circle>
                        <circle cx="22" cy="22" r="8">
                            <animate attributeName="r"
                                 begin="0s" dur="1.5s"
                                 values="6;1;2;3;4;5;6"
                                 calcMode="linear"
                                 repeatCount="indefinite" />
                        </circle>
                    </g>
                </svg>
            </div>
           
        </div>
    </div>
</template>


<style>
/* DROPZONE AREA */
.dropzone_area{
    display: grid;
    grid-template-rows: 200px auto;
    background: #bdbdbd;
    border-style: dashed;
    border-color: #828282;
}
.dropzone_text_hint{
    align-self: center;
    justify-self:center;

    font-family: fantasy;
    font-size: xx-large;
    color: #e4e4e4;
    cursor: pointer;
}
.epub_list{
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    grid-auto-rows: minmax(150px, auto);
    grid-gap: 10px; 
    margin: 10px;
}
.epub_list:hover {
    cursor: auto;
}
.epub{
    display: grid;

    background: #e6e6e6;
    border:1px solid white;

}
.epub .btns{
    width: 24px;
    height: 24px;
}
.epub .btns:hover{
    cursor: pointer;
    stroke: #00bcd4;
}
.epub .btns:active{
    stroke: initial;
}
.epub .show_conversions{
    grid-column-start: 1;
    grid-row-start: 1;
    margin: 4px;
}
.epub .delete{
    grid-column-start: 2;
    justify-self: end;
    margin: 4px;
}
.epub .title{
    grid-column-start: 1;
    grid-column-end: 3;
    justify-self: center;
    padding: 10px;
}
.epub .download{
    grid-column-start: 1;
    grid-column-end: 3;
    justify-self: center;
}
.epub .loader{
    justify-self:center;
    grid-column-start: 1;
    grid-column-end: 3;
}
</style>