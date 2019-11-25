new Chartist.Line('#chart-with-area', {
    labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    series: [
        [1000, 3500, 700, 1200, 500, 0, 4000]
    ]
}, {
    low: 0,
    showArea: true,
    lineSmooth: Chartist.Interpolation.simple({
        divisor: 2,
        fillHoles: false
    }),
    plugins: [
        Chartist.plugins.tooltip()
    ]
});