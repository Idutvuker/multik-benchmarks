package org.sample

import jcuda.runtime.JCuda
import org.jetbrains.kotlinx.multik.cuda.CudaEngine
import org.jetbrains.kotlinx.multik.cuda.linalg.CudaLinAlgEx
import org.jetbrains.kotlinx.multik.jni.linalg.NativeLinAlgEx
import org.jetbrains.kotlinx.multik.ndarray.data.get
import org.openjdk.jmh.annotations.*
import org.openjdk.jmh.infra.Blackhole

@State(Scope.Benchmark)
open class MatrixDotBenchmark {
//    @Param("100x1000", "100x5000", "100x10000", "1000x100", "5000x100", "10000x100", "1000x5000", "1000x10000", "5000x1000", "10000x1000")
    @Param("100x100", "500x500", "1000x1000", "5000x5000", "10000x10000")
    var shapeStr: String = ""

    lateinit var s: MathMatrixStructures

    @Setup
    fun setup() {
        val shape = shapeStr.split("x").map { it.toInt() }

        s = MathMatrixStructures(shape[0], shape[1])

        CudaEngine.initCuda()
    }

    @TearDown
    fun teardown() {
        CudaEngine.deinitCuda()
    }

    @Setup(Level.Iteration)
    fun setupIteration() {
        repeat(4) {
            System.gc()
            Thread.sleep(10)
        }

        CudaEngine.cacheCleanup()
    }

    @Benchmark
    fun multikCuda(bh: Blackhole) {
        bh.consume(CudaLinAlgEx.dotMM(s.multikMatrix1, s.multikMatrix2))
        JCuda.cudaDeviceSynchronize()
    }

    @Benchmark
    fun multikCudaWithCopyToHost(bh: Blackhole) {
        bh.consume(CudaLinAlgEx.dotMM(s.multikMatrix1, s.multikMatrix2)[0, 0])
    }

    @Benchmark
    fun multikNative(bh: Blackhole) {
        bh.consume(NativeLinAlgEx.dotMM(s.multikMatrix1, s.multikMatrix2))
    }

    @Benchmark
    fun nd4j(bh: Blackhole) {
        bh.consume(s.nd4jMatrix1.mmul(s.nd4jMatrix2))
    }
}