Vue.createApp({
    components: {
        VForm: VeeValidate.Form,
        VField: VeeValidate.Field,
        ErrorMessage: VeeValidate.ErrorMessage,
    },
    data() {
        return {
            RegSchema: {
                reg: (value) => {
                    if (value) {
                        return true;
                    }
                    return 'Поле не заполнено';
                },
                email_format: (value) => {
                    const regex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i
                    if (!value) {
                        return true;
                    }
                    if (!regex.test(value)) {

                        return '⚠ Формат почты нарушен';
                    }
                    return true;
                },
                code_format: (value) => {
                    const regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$/
                    if (!value) {
                        return true;
                    }
                    if (!regex.test(value)) {

                        return '⚠ Не менее 8 латинских символов или цифр в разных регистрах';
                    }
                    return true;
                }
            },
            Step: 'Number',
            RegInput: '',
            EnteredNumber: ''
        }
    },
    methods: {
        RegSubmit() {
            if (this.Step === 'Number') {
                this.Step = 'Code'

                console.log('Введённый номер:', this.RegInput)
                this.EnteredNumber = this.RegInput
                this.RegInput = ''
            }
            else {
                this.Step = 'Finish'
                console.log('Введённый код:', this.RegInput)
                this.EnteredCode = this.RegInput

                let body = JSON.stringify({
                    email: this.EnteredNumber,
                    password: this.EnteredCode,
                }, null, 2)

                console.log(body)

                let csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0]

                const requestOptions = {
                    method: "POST",
                    headers: { "Content-Type": "application/json", "X-CSRFToken": csrf_token.getAttribute("value") },
                    body: body
                };
                fetch("/login/", requestOptions)
                    .then((response) => {
                        return response.json();
                    })
                    .then((data) => {
                        this.RegInput = data['message'];
                        return data;
                    })
                    .then((data) => {
                            setTimeout((data) => {
                            if (data['message'] === 'Неверный пароль') {
                                 this.Step = 'Code';
                                 this.RegInput = '';
                            }
                            else {
                                location.replace(data['redirect']);
                            }
                        }, 2000, data)
                    });
            }
        },
        ToRegStep1() {
            this.Step = 'Number'
            this.RegInput = this.EnteredNumber
        },
        Reset() {
            this.Step = 'Number'
            this.RegInput = ''
            EnteredNumber = ''
        }
    }
}).mount('#RegModal')