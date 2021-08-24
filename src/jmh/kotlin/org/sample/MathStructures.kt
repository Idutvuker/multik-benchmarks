package org.sample

import org.jetbrains.kotlinx.multik.api.Multik
import org.jetbrains.kotlinx.multik.api.ndarray
import org.nd4j.linalg.factory.Nd4j
import kotlin.random.Random

class MathMatrixStructures(val rows: Int, val cols: Int) {
    val src1 = Array(rows) { FloatArray(cols) { RANDOM.nextFloat() } }
    val src2 = Array(cols) { FloatArray(rows) { RANDOM.nextFloat() } }

    val multikMatrix1 = Multik.ndarray(src1.map { it.toList() })
    val multikMatrix2 = Multik.ndarray(src2.map { it.toList() })

    val nd4jMatrix1 = Nd4j.create(src1)
    val nd4jMatrix2 = Nd4j.create(src2)
}

private val RANDOM = Random(42)