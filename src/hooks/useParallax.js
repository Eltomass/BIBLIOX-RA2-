import { useEffect, useRef, useState } from 'react';

const isMobile = () => typeof window !== 'undefined' && window.matchMedia && window.matchMedia('(max-width: 640px)').matches;

export const useParallax = (speed = 0.3, enabled = true) => {
  const [offset, setOffset] = useState(0);
  const raf = useRef(null);

  useEffect(() => {
    if (!enabled || isMobile()) return;

    const onScroll = () => {
      if (raf.current) cancelAnimationFrame(raf.current);
      raf.current = requestAnimationFrame(() => {
        setOffset(window.pageYOffset * speed);
      });
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    return () => {
      window.removeEventListener('scroll', onScroll);
      if (raf.current) cancelAnimationFrame(raf.current);
    };
  }, [speed, enabled]);

  return offset;
};
