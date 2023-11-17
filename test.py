from Interpreter import Interpreter, Memory
from Visualizer import Visualizer
from Devisualizer import Devisualizer
from optimize import brainfuck_loop_unroll
import time

from programs import predefined_programs


def test(program_name, number_of_loops=100000):
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


test("Hello World 1")
test("Hello World 2")
