import math
input = 1
learning_rate = 3
output_desire = 0
iterações = 0
input_weight = 2

def activation(soma):
    if soma >= 0:
        return 1
    else:
        return 0


soma = input * input_weight
output = activation(soma)
error = output_desire - output

while error != 0:
    iterações += 1
    soma = input * input_weight
    output = activation(soma)
    error = output_desire - output

    print("entrada", input, "desejada", output_desire)
    print("saída", output)
    print("erro", error)
    
    if error != 0:
        input_weight = input_weight + (learning_rate * error * input)
        print("######## Iterações:", iterações, " ###########")

print("Aprendeu")