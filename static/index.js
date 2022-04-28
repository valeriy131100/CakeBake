Vue.createApp({
    name: "App",
    components: {
        VForm: VeeValidate.Form,
        VField: VeeValidate.Field,
        ErrorMessage: VeeValidate.ErrorMessage,
    },
    data() {
        let components = JSON.parse(document.getElementById("cake-components").textContent)

        console.log(components)

        return {
            schema1: {
                lvls: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' количество уровней';
                },
                form: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' форму торта';
                },
                topping: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' топпинг';
                }
            },
            schema2: {
                name: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' имя';
                },
                phone: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' телефон';
                },
                email_format: (value) => {
                    const regex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат почты нарушен';
                    }
                    return true;
                },
                phone_format:(value) => {
                    const regex = /^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$/
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат телефона нарушен';
                    }
                    return true;
                },
                email: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' почту';
                },
                address: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' адрес';
                },
                date: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' дату доставки';
                },
                time: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' время доставки';
                }
            },
            DATA: {
                Levels: components['levels']['list'],
                Forms: components['forms']['list'],
                Toppings: components['toppings']['list'],
                Berries: components['berries']['list'],
                Decors: components['decors']['list']
            },
            Costs: {
                Levels: components['levels']['costs'],
                Forms: components['forms']['costs'],
                Toppings: components['toppings']['costs'],
                Berries: components['berries']['costs'],
                Decors: components['decors']['costs'],
                Words: 500
            },
            Levels: 0,
            Form: 0,
            Topping: 0,
            Berries: 0,
            Decor: 0,
            Words: '',
            Comments: '',
            Designed: false,

            Name: '',
            Phone: null,
            Email: null,
            Address: null,
            Dates: null,
            Time: null,
            DelivComments: ''
        }
    },
    methods: {
        ToStep4() {
            this.Designed = true
            setTimeout(() => this.$refs.ToStep4.click(), 0);

        },
        SubmitOrder() {
            let body = JSON.stringify({
                Cost: this.Cost,
                Levels: this.DATA.Levels[this.Levels],
                Form: this.DATA.Forms[this.Form],
                Topping: this.DATA.Toppings[this.Topping],
                Berries: this.DATA.Berries[this.Berries],
                Decor: this.DATA.Decors[this.Decor],
                Words: this.Words,
                Comments: this.Comments,
                Name: this.Name,
                Phone: this.Phone,
                Email: this.Email,
                Address: this.Address,
                Dates: this.Dates,
                Time: this.Time,
                DelivComments: this.DelivComments,
            }, null ,2)

            console.log(body)

            let csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0]

            const requestOptions = {
                method: "POST",
                headers: {"Content-Type": "application/json", "X-CSRFToken": csrf_token.getAttribute("value")},
                body: body
            };
            fetch("/payment/", requestOptions)
                .then((response) => {
                    return response.json();
                })
                .then((data) => {
                    console.log(data);
                    window.location.replace(data['redirect']);
                });
        }
    },
    computed: {
        Cost() {
            let W = this.Words ? this.Costs.Words : 0
            return this.Costs.Levels[this.Levels] + this.Costs.Forms[this.Form] +
                this.Costs.Toppings[this.Topping] + this.Costs.Berries[this.Berries] +
                this.Costs.Decors[this.Decor] + W
        }
    }
}).mount('#VueApp')