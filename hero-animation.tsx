"use client"

import { useRef } from "react"
import { Canvas, useFrame } from "@react-three/fiber"
import { OrbitControls, Environment, Float } from "@react-three/drei"
import type * as THREE from "three"

function ResumeModel() {
  const group = useRef<THREE.Group>(null)

  // Create a simple resume model with Three.js
  useFrame((state) => {
    if (group.current) {
      group.current.rotation.y = state.clock.getElapsedTime() * 0.1
    }
  })

  return (
    <group ref={group}>
      <Float speed={1.5} rotationIntensity={0.2} floatIntensity={0.5}>
        {/* Paper base */}
        <mesh position={[0, 0, 0]} castShadow receiveShadow>
          <boxGeometry args={[8, 11, 0.1]} />
          <meshStandardMaterial color="#f8f9fa" roughness={0.1} metalness={0.1} />
        </mesh>

        {/* Header section */}
        <mesh position={[0, 4.5, 0.06]} castShadow>
          <boxGeometry args={[7, 1, 0.05]} />
          <meshStandardMaterial color="#4f46e5" roughness={0.3} />
        </mesh>

        {/* Content lines */}
        {[-3, -1.5, 0, 1.5, 3].map((y, i) => (
          <mesh key={i} position={[0, y, 0.06]} castShadow>
            <boxGeometry args={[7, 0.4, 0.02]} />
            <meshStandardMaterial color="#e2e8f0" roughness={0.5} />
          </mesh>
        ))}
      </Float>
    </group>
  )
}

export default function HeroAnimation() {
  return (
    <div className="w-full h-full absolute opacity-70">
      <Canvas shadows camera={{ position: [0, 0, 16], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} intensity={1} castShadow />
        <ResumeModel />
        <Environment preset="city" />
        <OrbitControls enableZoom={false} enablePan={false} enableRotate={false} />
      </Canvas>
    </div>
  )
}

