Vue.createApp({
    components: {
        VForm: VeeValidate.Form,
        VField: VeeValidate.Field,
        ErrorMessage: VeeValidate.ErrorMessage,
    },
    data() {
        return {
            Edit: false,
            Name: '',
            Phone: '',
            Email: '',
            Schema: {
                name_format: (value) => {
                    const regex = /^[a-zA-Zа-яА-я\s\.\-]+$/
                    if (!value) {
                        return '⚠ Поле не может быть пустым';
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Недопустимые символы в имени';
                    }
                    return true;
                },
                phone_format: (value) => {
                    const regex = /^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$/
                    if (!value) {
                        return '⚠ Поле не может быть пустым';
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат телефона нарушен';
                    }
                    return true;
                },
                email_format: (value) => {
                    const regex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i
                    if (!value) {
                        return '⚠ Поле не может быть пустым';
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат почты нарушен';
                    }
                    return true;
                }
            }
        }
    },
    methods: {
        ApplyChanges() {
            this.Edit = false
            console.log(this.Name, this.Phone, this.Email)
        }
    },
    created() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
      body: JSON.stringify({ action: 'load' })
    };
    fetch('/profile/', requestOptions)
    .then(async response => {
      const data = await response.json();
      // check for error response
      if (!response.ok) {
        // get error message from body or default to response status
        const error = (data && data.message) || response.status;
        return Promise.reject(error);
      }
      this.Name = data['user_first_name'];
      this.Phone = data['user_phone'];
      this.Email = data['user_email'];
    })
    .catch(error => {
      this.errorMessage = error;
      console.error('There was an error!', error);
    });
}
}).mount('#LK')