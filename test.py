from Interpreter import Interpreter, Memory
from Visualizer import Visualizer
from Devisualizer import Devisualizer
from optimize import brainfuck_loop_unroll
import time

from programs import predefined_programs
from optimize import memory_range_analysis_1, memory_range_analysis_2


def test(program_name, number_of_loops=100):
    bfp = predefined_programs[program_name]

    print(f"Running test: {program_name}")

    # Don't touch!!!
    vis = Visualizer(bfp)
    vis.bfp_to_graph_compressed()
    devis = Devisualizer(vis)

    devis_bfp = devis.bfp
    loop_unroll_bfp = brainfuck_loop_unroll(bfp)

    # The process itself
    print(f"Running base program {number_of_loops} times")

    total_runtime = 0
    for i in range(number_of_loops):
        start = time.time()
        inte = Interpreter(Memory())
        inte.run(bfp)
        end = time.time()
        runtime = end - start
        total_runtime += runtime

    mean_runtime_bfp = total_runtime / number_of_loops

    print(f"Mean runtime of base program is {mean_runtime_bfp}")
    print()

    print(f"Running Devisualized program {number_of_loops} times")
    total_runtime = 0
    for i in range(number_of_loops):
        start = time.time()
        inte = Interpreter(Memory())
        inte.run(devis_bfp)
        end = time.time()
        runtime = end - start
        total_runtime += runtime

    mean_runtime_devis_bfp = total_runtime / number_of_loops

    print(f"Mean runtime of devisualized program is {mean_runtime_devis_bfp}")
    print()

    print(f"Running loop unrolled program {number_of_loops} times")
    total_runtime = 0
    for i in range(number_of_loops):
        start = time.time()
        inte = Interpreter(Memory())
        inte.run(loop_unroll_bfp)
        end = time.time()
        runtime = end - start
        total_runtime += runtime

    mean_runtime_loop_unroll_bfp = total_runtime / number_of_loops

    print(f"Mean runtime of loop unrolled program is {mean_runtime_loop_unroll_bfp}")


# test("Hello World 1")
# test("Hello World 2")
# test("Squares")
# test("Redundancy 1")


def memory_prediction_test(program_name):
    mem = Memory()
    inte = Interpreter(mem)
    inte.run(predefined_programs[program_name])
    max_mem = mem.max
    amount = inte.memory.max_pointer + 1

    print("Memory prediction test")
    print(f"Max actual: {max_mem[:amount]}")

    predicted_mem = memory_range_analysis_1(predefined_programs[program_name], amount)
    max_predicted = []
    min_predicted = []
    for i in range(amount):
        max_predicted.append(max(predicted_mem[i]))
        min_predicted.append(min(predicted_mem[i]))

    correct = 0
    for i in range(amount):
        if max_mem[i] <= max_predicted[i] and max_mem[i] >= min_predicted[i]:
            correct += 1
    avg_rpe = 0
    for i in range(amount):
        if max_mem[i] != 0:
            avg_rpe += (
                abs(max_predicted[i] - max_mem[i] - min_predicted[i]) / max_mem[i]
            )
        else:
            avg_rpe += 1

    avg_rpe /= amount

    print(f"Min predicted (1): {min_predicted[:amount]}")
    print(f"Max predicted (1): {max_predicted[:amount]}")
    print(f"Average RPE: {avg_rpe}")
    print(f"Correct predictions: {correct}/{amount}")

    predicted_mem = memory_range_analysis_2(predefined_programs[program_name], amount)
    max_predicted = []
    min_predicted = []
    for i in range(amount):
        max_predicted.append(max(predicted_mem[i]))
        min_predicted.append(min(predicted_mem[i]))

    correct = 0
    for i in range(amount):
        if max_mem[i] <= max_predicted[i] and max_mem[i] >= min_predicted[i]:
            correct += 1

    avg_rpe = 0
    for i in range(amount):
        if max_mem[i] != 0:
            avg_rpe += (
                abs(max_predicted[i] - max_mem[i] - min_predicted[i]) / max_mem[i]
            )
        else:
            avg_rpe += 1

    avg_rpe /= amount
    print(f"Min predicted (2): {min_predicted[:amount]}")
    print(f"Max predicted (2): {max_predicted[:amount]}")
    print(f"Average RPE: {avg_rpe}")
    print(f"Correct predictions: {correct}/{amount}")


# memory_prediction_test("Redundancy 1")
