webpackJsonp([1],{"/TfF":function(e,n){},"20Zl":function(e,n){},HdV5:function(e,n){},NHnr:function(e,n,t){"use strict";Object.defineProperty(n,"__esModule",{value:!0});var o=t("7+uW"),i=t("rifk"),s=t.n(i),r=t("woOf"),a=t.n(r),c=t("mvHQ"),l=t.n(c),u={name:"file-uploader",props:["epubs"],methods:{handle_on_drop:function(e){var n=e.dataTransfer,t=null;if(n.items&&n.items.length>0)for(var o=0;o<n.items.length;o++)t=n.items[o].getAsFile(),this.processFile(t);else for(o=0;o<n.files.length;o++)t=n.files[o],this.processFile(t)},handle_on_drag_end:function(e){var n=ev.dataTransfer;if(n.items&&n.items.length>0)for(var t=0;t<n.items.length;t++)n.items.remove(t);else n.clearData()},handle_click:function(e){this.$refs.file_input.click()},handle_file_input_change:function(e){console.log("input change event:",e);for(var n=e.target.files,t=0;t<n.length;t++)this.processFile(n[t]);e.target.value=null},processFile:function(e){if(console.log("Processing file:",e),"application/epub+zip"==e.type){var n=new FileReader;n.readAsDataURL(e),n.onerror=function(e){console.error(e)},n.onload=function(n){var t={name:e.name,bin_data:n.target.result};BUS.$emit("add_epub_file",t)}}else TOAST.error({message:e.name+" is not supported. Epub files only."})},download_epub:function(e){console.log("downloading:",e),location.replace("http://localhost:7000/download_epub/"+e)},handle_delete_epub:function(e){BUS.$emit("remove_epub",e)}}},d={render:function(){var e=this,n=e.$createElement,t=e._self._c||n;return t("div",{staticClass:"dropzone_area",on:{dragover:function(e){e.preventDefault()},drop:function(n){n.preventDefault(),e.handle_on_drop(n)},dragend:e.handle_on_drag_end}},[t("input",{ref:"file_input",staticStyle:{display:"none"},attrs:{type:"file",multiple:"",accept:"application/epub+zip"},on:{change:e.handle_file_input_change}}),e._v(" "),t("p",{staticClass:"dropzone_text_hint",on:{click:e.handle_click}},[e._v("Click here or drag files to upload")]),e._v(" "),t("div",{staticClass:"epub_list"},e._l(e.epubs,function(n,o,i){return t("div",{key:i,staticClass:"epub"},[t("svg",{staticClass:"btns show_conversions",attrs:{xmlns:"http://www.w3.org/2000/svg",width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",stroke:"black","stroke-width":"2","stroke-linecap":"round","stroke-linejoin":"round"},on:{click:function(n){e.$modal.show("conversions",o)}}},[t("line",{attrs:{x1:"8",y1:"6",x2:"21",y2:"6"}}),t("line",{attrs:{x1:"8",y1:"12",x2:"21",y2:"12"}}),e._v(" "),t("line",{attrs:{x1:"8",y1:"18",x2:"21",y2:"18"}}),t("line",{attrs:{x1:"3",y1:"6",x2:"3",y2:"6"}}),e._v(" "),t("line",{attrs:{x1:"3",y1:"12",x2:"3",y2:"12"}}),t("line",{attrs:{x1:"3",y1:"18",x2:"3",y2:"18"}})]),e._v(" "),t("svg",{staticClass:"btns delete",attrs:{xmlns:"http://www.w3.org/2000/svg",width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",stroke:"black","stroke-width":"1.5","stroke-linecap":"round","stroke-linejoin":"round"},on:{click:function(n){e.handle_delete_epub(o)}}},[t("circle",{attrs:{cx:"12",cy:"12",r:"10"}}),e._v(" "),t("line",{attrs:{x1:"15",y1:"9",x2:"9",y2:"15"}}),e._v(" "),t("line",{attrs:{x1:"9",y1:"9",x2:"15",y2:"15"}})]),e._v(" "),t("span",{staticClass:"title"},[e._v(e._s(o))]),e._v(" "),n.ready?t("svg",{staticClass:"btns download",attrs:{xmlns:"http://www.w3.org/2000/svg",width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",stroke:"black","stroke-width":"2","stroke-linecap":"round","stroke-linejoin":"round"},on:{click:function(n){e.download_epub(o)}}},[t("polyline",{attrs:{points:"8 17 12 21 16 17"}}),e._v(" "),t("line",{attrs:{x1:"12",y1:"12",x2:"12",y2:"21"}}),e._v(" "),t("path",{attrs:{d:"M20.88 18.09A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.29"}})]):t("svg",{staticClass:"loader",attrs:{width:"45",height:"45",viewBox:"0 0 45 45",xmlns:"http://www.w3.org/2000/svg",stroke:"#00bcd4"}},[t("g",{attrs:{fill:"none","fill-rule":"evenodd",transform:"translate(1 1)","stroke-width":"2"}},[t("circle",{attrs:{cx:"22",cy:"22",r:"6","stroke-opacity":"0"}},[t("animate",{attrs:{attributeName:"r",begin:"1.5s",dur:"3s",values:"6;22",calcMode:"linear",repeatCount:"indefinite"}}),e._v(" "),t("animate",{attrs:{attributeName:"stroke-opacity",begin:"1.5s",dur:"3s",values:"1;0",calcMode:"linear",repeatCount:"indefinite"}}),e._v(" "),t("animate",{attrs:{attributeName:"stroke-width",begin:"1.5s",dur:"3s",values:"2;0",calcMode:"linear",repeatCount:"indefinite"}})]),e._v(" "),t("circle",{attrs:{cx:"22",cy:"22",r:"6","stroke-opacity":"0"}},[t("animate",{attrs:{attributeName:"r",begin:"3s",dur:"3s",values:"6;22",calcMode:"linear",repeatCount:"indefinite"}}),e._v(" "),t("animate",{attrs:{attributeName:"stroke-opacity",begin:"3s",dur:"3s",values:"1;0",calcMode:"linear",repeatCount:"indefinite"}}),e._v(" "),t("animate",{attrs:{attributeName:"stroke-width",begin:"3s",dur:"3s",values:"2;0",calcMode:"linear",repeatCount:"indefinite"}})]),e._v(" "),t("circle",{attrs:{cx:"22",cy:"22",r:"8"}},[t("animate",{attrs:{attributeName:"r",begin:"0s",dur:"1.5s",values:"6;1;2;3;4;5;6",calcMode:"linear",repeatCount:"indefinite"}})])])])])}))])},staticRenderFns:[]},_=t("VU/8")(u,d,!1,function(e){t("/TfF")},null,null).exports,p={name:"unit-selector",props:["conversionUnit"],methods:{set_conversion_unit:function(e){BUS.$emit("set_conversion_unit",e)}}},v={render:function(){var e=this,n=e.$createElement,t=e._self._c||n;return t("div",{staticClass:"menu"},[t("div",{staticClass:"menu_items"},[t("button",{class:"metric"==e.conversionUnit?"active":"",attrs:{title:"Convert Units to Metric System"},on:{click:function(n){e.set_conversion_unit("metric")}}},[e._v("Metric")]),e._v(" "),t("button",{class:"imperial"==e.conversionUnit?"active":"",attrs:{title:"Convert Units to Imperial System"},on:{click:function(n){e.set_conversion_unit("imperial")}}},[e._v("Imperial")])])])},staticRenderFns:[]},f=t("VU/8")(p,v,!1,null,null,null).exports,m=t("YxSy"),h=t.n(m);t("20Zl");window.TOAST=h.a;var b={name:"app",components:{fileUploader:_,unitSelector:f},data:function(){return{conversion_unit:"metric",epubs:{},show_conversions_for_epub:[]}},methods:{handle_before_open_conversions:function(e){this.epubs[e.params]&&(console.log("loading conversions..."),this.show_conversions_for_epub=this.epubs[e.params].conversions)}},mounted:function(){var e=this;WS.onopen=function(n){WS.send(l()({do:"set_conversion_unit",with:e.conversion_unit}))},BUS.$on("set_conversion_unit",function(n){e.conversion_unit=n,WS.send(l()({do:"set_conversion_unit",with:n})),console.log("conversion unit set to:",n)}),BUS.$on("add_epub_file",function(n){if(e.epubs[n.name])TOAST.warning({message:"File already added.",timeout:2e3});else{console.log("adding new epub file:",n);var t={};t[n.name]={ready:!1,conversions:[]},e.epubs=a()({},e.epubs,t),WS.send(l()({do:"convert_epub",with:n}))}}),BUS.$on("epub_conversion_completed",function(n){0==n.num_of_changes?(TOAST.info({message:"No conversion needed for "+n.name+".."}),BUS.$emit("remove_epub",n.name)):(TOAST.success({message:n.name+" conversion completed with "+n.num_of_changes+" change(s)"}),e.epubs[n.name].ready=!0)}),BUS.$on("show_current_epubs",function(n){e.epubs=a()({},e.epubs,n)}),BUS.$on("conversion_update",function(n){e.epubs[n.file].conversions.push(n.conversion)}),BUS.$on("notify_current_conversion_unit",function(n){e.conversion_unit=n}),BUS.$on("remove_epub",function(n){e.$delete(e.epubs,n),WS.send(l()({do:"remove_epub",with:n}))})}},w={render:function(){var e=this,n=e.$createElement,t=e._self._c||n;return t("div",{attrs:{id:"app"}},[t("div",{staticClass:"header"},[e._m(0),e._v(" "),t("unit-selector",{attrs:{"conversion-unit":e.conversion_unit}})],1),e._v(" "),t("file-uploader",{attrs:{epubs:e.epubs}}),e._v(" "),t("modal",{attrs:{name:"conversions",draggable:!0,scrollable:!0,height:"auto"},on:{"before-open":e.handle_before_open_conversions,closed:function(n){e.show_conversions_for_epub=[]}}},[t("div",{staticClass:"list_of_conversions"},[t("p",{staticClass:"title"},[e._v("List of conversions:")]),e._v(" "),e._l(e.show_conversions_for_epub,function(n,o){return t("span",{key:o,staticClass:"list_items"},[e._v("\n        "+e._s(n)+"\n      ")])})],2)])],1)},staticRenderFns:[function(){var e=this.$createElement,n=this._self._c||e;return n("div",{staticClass:"project_name"},[n("span",[this._v("Epub Unit Converter")])])}]},g=t("VU/8")(b,w,!1,function(e){t("HdV5")},null,null).exports;o.a.use(s.a),o.a.config.productionTip=!1,window.BUS=new o.a,window.WS=new WebSocket("ws://localhost:7000/wakey_wakey"),new o.a({el:"#app",components:{App:g},template:"<App/>"}),WS.onmessage=function(e){var n=null;try{n=JSON.parse(e.data)}catch(n){console.log("Unstructered Message from server:",e.data)}if(n)switch(console.log("Msg from server:",n),n.do){case"notify_epub_conversion_completed":BUS.$emit("epub_conversion_completed",n.with);break;case"show_current_epubs":BUS.$emit("show_current_epubs",n.with);break;case"notify_conversion_update":BUS.$emit("conversion_update",n.with);break;case"show_current_conversion_unit":BUS.$emit("notify_current_conversion_unit",n.with)}},WS.onerror=function(e){console.error("WS error:",e),TOAST.error({message:"Error with the cli. Make sure it's running."})}}},["NHnr"]);
//# sourceMappingURL=app.9d7687db8bc5f2c7e886.js.map