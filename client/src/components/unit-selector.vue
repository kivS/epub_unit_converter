<script>
    export default{
        name: 'unit-selector',
        props:['conversionUnit'],
        methods:{
            set_conversion_unit: function(unit){
                BUS.$emit('set_conversion_unit', unit)
            }
        }
    }
</script>

<template>
  <div class="menu">
       <div class="menu_items">
           <button @click="set_conversion_unit('metric')" title="Convert Units to Metric System" :class="conversionUnit == 'metric'? 'active':'' ">Metric</button>
           <button @click="set_conversion_unit('imperial')" title="Convert Units to Imperial System" :class="conversionUnit == 'imperial'? 'active':'' ">Imperial</button>
       </div>
  </div> 
</template>