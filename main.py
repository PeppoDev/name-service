import consumers.client

consumers.client.request(
    "imc_calc", {'weight': '80', 'height': '170'})

consumers.client.request(
    "cpf_validation", {'cpf': '12345678901'})
