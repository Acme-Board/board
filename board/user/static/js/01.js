const app = new Vue({
    el: '#app',
    data: {
        meses: '',
        total: 0
    },
    methods:{

    },
    computed: {
        totalPremium(){
            this.total = this.meses * 3,99;
            return this.total;
        }
    }
})