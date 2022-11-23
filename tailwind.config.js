module.exports = {
      future: {
        removeDeprecatedGapUtilities: true,
        purgeLayersByDefault: true,
    },
    purge: {
        enabled: false, //true for production build
        content: [
            '../**/templates/*.html',
            '../**/templates/**/*.html'
        ]
    },
  // content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {
      spacing: {
        "25vh": "25vh",
        "50vh": "50vh",
        "75vh": "75vh"
      },
      borderRadius: {
        xl: "1.5rem"
      },
      minHeight: {
        "50vh": "50vh",
        "75vh": "75vh"
      }
    }
  },
  variants: {},
  plugins: {
          tailwindcss: {},
    autoprefixer: {}
  }
};
