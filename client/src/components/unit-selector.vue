<script>
    export default{
        name: 'unit-selector',
        methods:{
            set_conversion_unit: function(unit){
                BUS.$emit('set_conversion_unit', unit)
            }
        }
    }
</script>

<template>
   <div>
       <h3>Convert Ebook to</h3>
       <button @click="set_conversion_unit('metric')">Metric System</button>
       <button  @click="set_conversion_unit('imperial')">Imperial System</button>
   </div>
</template>