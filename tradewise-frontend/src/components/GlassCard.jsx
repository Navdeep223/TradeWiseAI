function GlassCard({ children, className = "" }) {
  return (
    <div
      className={`
        relative
        bg-white/8
        backdrop-blur-2xl
        border border-white/20
        rounded-3xl
        shadow-[0_40px_100px_rgba(0,0,0,0.7)]
        overflow-hidden
        ${className}
      `}
    >
      {/* Light reflection overlay */}
      <div className="absolute inset-0 rounded-3xl bg-gradient-to-br from-white/20 to-transparent opacity-20 pointer-events-none"></div>

      <div className="relative z-10">
        {children}
      </div>
    </div>
  );
}

export default GlassCard;