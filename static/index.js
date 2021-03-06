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
            Pks: {
                Levels: components['levels']['pks'],
                Forms: components['forms']['pks'],
                Toppings: components['toppings']['pks'],
                Berries: components['berries']['pks'],
                Decors: components['decors']['pks'],
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
            let advertising_company = JSON.parse(document.getElementById("advertising-company").textContent)

            let body = JSON.stringify({
                cake: {
                    title: "Созданный пользователем торт",
                    levels: this.Pks.Levels[this.Levels],
                    form: this.Pks.Forms[this.Form],
                    topping: this.Pks.Toppings[this.Topping],
                    berry: this.Pks.Berries[this.Berries],
                    decor: this.Pks.Decors[this.Decor],
                    text: this.Words
                },
                comment: this.Comments,
                name: this.Name,
                phone_number: this.Phone,
                email: this.Email,
                delivery_address: this.Address,
                delivery_date: this.Dates,
                delivery_time: this.Time,
                delivery_comment: this.DelivComments,
                advertising_company: advertising_company
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
                    window.location.replace(data['redirect']);
                });
        }
    },
    created() {
        fetch('/user_data/')
        .then(async response => {
          const data = await response.json();
          // check for error response
          if (!response.ok) {
            // get error message from body or default to response status
            const error = (data && data.message) || response.status;
            return Promise.reject(error);
          }
          this.Name = data['user_first_name'];
          this.Phone = data['user_phone_number'];
          this.Email = data['user_email'];
          this.Address = data['user_address'];
        })
        .catch(error => {
          this.errorMessage = error;
//          console.error("There was an error!", error);
        });
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