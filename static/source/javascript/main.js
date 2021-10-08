$(document).ready(function () {
  // initiating html input range plugin
  // htmlInputrange.default();
  // if you want to customize html input range plugin
  htmlInputRange.options({
    tooltip: true,
    max: 90,
    labels: true,
    labelsData: {
      one: 'one',
      two: 'two'
    }
  });
});