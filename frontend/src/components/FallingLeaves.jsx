import { useEffect, useState } from "react";
import mapleLeafImg from "../assets/maple-leaf.png";

const FallingLeaves = () => {
  const [leaves, setLeaves] = useState([]);
  const MAX_LEAVES = 12; // Increased from ~3-4 to make it more fall-ish

  useEffect(() => {
    const timeouts = new Set(); // Track all timeouts for cleanup

    const createLeaf = () => {
      const id = Date.now() + Math.random();
      const leaf = {
        id,
        left: Math.random() * 100,
        animationDelay: Math.random() * 2,
        animationDuration: Math.random() * 3 + 6, // 6-9 seconds
        size: 30 + Math.random() * 25, // 30-55px
        opacity: 0.6 + Math.random() * 0.3, // 0.6-0.9
      };

      setLeaves((prev) => {
        // If we're at max capacity, remove the oldest leaf and add new one
        if (prev.length >= MAX_LEAVES) {
          return [...prev.slice(1), leaf]; // Remove first, add new at end
        }
        return [...prev, leaf];
      });

      // Remove leaf after animation completes
      const timeoutId = setTimeout(
        () => {
          setLeaves((prev) => prev.filter((l) => l.id !== id));
          timeouts.delete(timeoutId); // Clean up timeout reference
        },
        (leaf.animationDuration + leaf.animationDelay) * 1000,
      );

      timeouts.add(timeoutId); // Track timeout for cleanup
    };

    // Create initial leaves (start with a few for immediate effect)
    for (let i = 0; i < 3; i++) {
      setTimeout(() => createLeaf(), i * 500); // Stagger initial leaves
    }

    // Create new leaves more frequently for more fall-ish effect
    const interval = setInterval(createLeaf, 2000); // Reduced from 3000 to 2000ms

    return () => {
      clearInterval(interval);
      // Clear all pending timeouts
      timeouts.forEach((timeout) => clearTimeout(timeout));
      timeouts.clear();
    };
  }, []);

  return (
    <div className="falling-leaves-container">
      {leaves.map((leaf) => (
        <div
          key={leaf.id}
          className="falling-leaf"
          style={{
            left: `${leaf.left}vw`,
            animationDelay: `${leaf.animationDelay}s`,
            animationDuration: `${leaf.animationDuration}s`,
            width: `${leaf.size}px`,
            height: `${leaf.size}px`,
            opacity: leaf.opacity,
            backgroundImage: `url(${mapleLeafImg})`,
          }}
        />
      ))}
    </div>
  );
};

export default FallingLeaves;
