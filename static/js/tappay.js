function tappayDealWith() {
   TPDirect.setupSDK(20254, 'app_OJvQf0k7VFRyQgrs8HQYLXgYTcPr1WF4HBarLQ9a0xlaHFG0FPF5GCruoSnW', 'sandbox');

   TPDirect.card.setup({
      fields: {
         number: {
            element: '#card-number',
            placeholder: '**** **** **** ****'
         },
         expirationDate: {
            element: '#overdue-date',
            placeholder: 'MM / YY'
         },
         ccv: {
            element: '#verified-password',
            placeholder: 'ccv'
         }
      }
   });
   
   TPDirect.card.onUpdate(update => {
      // update.canGetPrime === true
      // --> you can call TPDirect.card.getPrime()   
      if (update.canGetPrime) {
         // Enable submit Button to get prime.
         // submitButton.removeAttribute('disabled')
      } else {
         // Disable submit Button to get prime.
         // submitButton.setAttribute('disabled', true)
      }
      
      // cardTypes = ['mastercard', 'visa', 'jcb', 'amex', 'unionpay','unknown']
      if (update.cardType === 'visa') {
   
      }
   
      // number 欄位是錯誤的
      if (update.status.number === 2) {
         // setNumberFormGroupToError()
      } else if (update.status.number === 0) {
         // setNumberFormGroupToSuccess()
      } else {
         // setNumberFormGroupToNormal()
      }
      
      if (update.status.expiry === 2) {
         // setNumberFormGroupToError()
      } else if (update.status.expiry === 0) {
         // setNumberFormGroupToSuccess()
      } else {
         // setNumberFormGroupToNormal()
      }
   
      if (update.status.ccv === 2) {
         // setNumberFormGroupToError()
      } else if (update.status.ccv === 0) {
         // setNumberFormGroupToSuccess()
      } else {
         // setNumberFormGroupToNormal()
      }
   
   });
}

export { tappayDealWith };