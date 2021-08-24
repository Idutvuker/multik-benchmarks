plugins {
    `java-library`
    kotlin("jvm") version "1.4.20"
    id("me.champeau.jmh") version "0.6.2"
}

repositories {
    mavenCentral()

    flatDir {
        dirs("libs")
    }
}

dependencies {
    implementation(kotlin("stdlib"))

    jmhImplementation("io.github.microutils:kotlin-logging:+")
    jmhImplementation("ch.qos.logback:logback-core:1.3.0-alpha9")
    jmhImplementation("ch.qos.logback:logback-classic:1.3.0-alpha9")

    jmhImplementation("org.jetbrains.kotlinx:multik-api:0.0.2")
    jmhImplementation("org.jetbrains.kotlinx:multik-cuda:0.0.2")
    jmhImplementation("org.jetbrains.kotlinx:multik-native:0.0.2")

    jmhImplementation("org.nd4j:nd4j-api:1.0.0-M1.1")
    jmhImplementation("org.nd4j:nd4j-cuda-11.2-platform:1.0.0-M1.1")

    jmhImplementation(kotlin("stdlib"))

}

tasks.withType<org.jetbrains.kotlin.gradle.tasks.KotlinCompile>().configureEach {
    kotlinOptions { jvmTarget = "11" }
}

jmh {
    jmhVersion.set("1.28")
    includeTests.set(false)
    duplicateClassesStrategy.set(DuplicatesStrategy.EXCLUDE)

    benchmarkMode.set(listOf("Throughput"))
    failOnError.set(true)
    humanOutputFile.set(File("jmh_output.txt"))

    jvmArgs.set(listOf("-Xms12g"))

    forceGC.set(true)

    fork.set(2)
    warmupIterations.set(3)
    warmup.set("1s")

    iterations.set(10)
    timeOnIteration.set("1s")
}

