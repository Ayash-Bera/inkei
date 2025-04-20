import React from 'react';
import { motion } from 'framer-motion';
import { BackgroundBeams } from '../ui/background-beams';
import Button from '../ui/button';

const container = {
  hidden: {},
  show: {
    transition: {
      staggerChildren: 0.3,
    },
  },
};

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  show: { opacity: 1, y: 0, transition: { duration: 0.8, ease: 'easeOut' } },
};

const Hero = () => {
  return (
    <section id="hero" className="relative h-screen w-full overflow-hidden flex items-center font-sans">
      <div className="h-full w-full bg-gradient-to-b from-[#1e1b4b] to-[#0f172a] relative flex flex-col items-center justify-center">
        <motion.div
          variants={container}
          initial="hidden"
          animate="show"
          className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center"
        >
          <motion.h1
            variants={fadeUp}
            className="text-4xl md:text-6xl lg:text-7xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-500 mb-6 leading-tight"
          >
            Elevate Your Digital Experience
          </motion.h1>

          <motion.p
            variants={fadeUp}
            className="text-slate-300 max-w-3xl mx-auto text-lg md:text-xl mb-8"
          >
            Explore a new dimension of digital solutions with our cutting-edge platform. 
            Streamlined workflows, powerful insights, and seamless integration to transform your business.
          </motion.p>

          <motion.div
            variants={fadeUp}
            className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-4 mt-8"
          >
            <Button variant="primary" size="large" className="min-w-32 sm:min-w-40 bg-purple-600 hover:bg-purple-700 text-white">
              Get Started
            </Button>
            <Button
              variant="outline"
              size="large"
              className="min-w-32 sm:min-w-40 border-purple-400 text-purple-200 hover:bg-purple-800 hover:border-purple-500"
            >
              Learn More
            </Button>
          </motion.div>

          <motion.div variants={fadeUp} className="mt-16 relative">
            <div className="absolute -inset-0.5 bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg blur-sm opacity-70"></div>
            <div className="relative bg-slate-900 rounded-lg overflow-hidden border border-slate-700 shadow-xl">
              <img 
                src="/api/placeholder/1200/600" 
                alt="Dashboard Preview" 
                className="w-full h-auto rounded-lg opacity-90 hover:opacity-100 transition-opacity duration-300"
              />
            </div>
          </motion.div>
        </motion.div>

        <BackgroundBeams />
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-10 left-1/2 transform -translate-x-1/2 z-10 animate-bounce">
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          width="32" 
          height="32" 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor"
          className="text-purple-300"
        >
          <path 
            strokeLinecap="round" 
            strokeLinejoin="round" 
            strokeWidth="2" 
            d="M19 14l-7 7m0 0l-7-7m7 7V3" 
          />
        </svg>
      </div>
    </section>
  );
};

export default Hero;
