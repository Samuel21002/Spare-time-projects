$(function() {   // Wait until the project is loaded
  
    console.log('Document loaded')
    let output = $('#id_fx_result')
  
    with (Math) {
      /* Makes the calculations utilizing the Math-library and returns an array of the function table */
      function make_fx(func, start, end, step) {
        let fx_array = [] // Array of object containing x and y values
        try {
          let x = start
  
          for (start; x < end; x += step) {   // Calculates the function and appends all x and y values as attributes	
            fx_array.push({
              x: Math.round(x * 10) / 10,
              y: parseFloat(eval(func))
            })
          }
          return fx_array
        } catch(e) {
          output.text('Cannot calculate the function').addClass('error')
          alert(`There was an error with calculating '${func}'!\n${e}`)
        }
      }
    }
  
    /* Draws the values to the canvas using Chart.js after separating all X and Y values as different arrays */
    function draw_fx(iterator) {
      let fx_values_x = []
      iterator.forEach((val) => {
        fx_values_x.push(val.x)
      })
      let fx_values_y = []
      iterator.forEach((val) => {
        fx_values_y.push(val.y)
      })
      let canv = document.getElementById('id_canv')
      let c = canv.getContext('2d')
      let chartStatus = Chart.getChart('id_canv')
      if (chartStatus != undefined) {
        chartStatus.destroy()
      }
      // Chart.js
      new Chart(c, {
        type: 'line',
        data: {
          labels: fx_values_x,
          datasets: [
            {
              label: `${$('#id_function').val()} `,
              fill: false,
              pointRadius: 4,
              borderColor: 'rgba(100,0,255,0.5)',
              data: fx_values_y,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          elements: {
            line: {
              borderJoinStyle: 'round',
              tension: 0.3,
              borderColor: 'red',
              radius: 5,
            },
          },
          plugins: {
            title: {
              display: true,
              text: 'Function graph',
            },
            zoom:{
              zoom: {
                wheel: {
                  enabled: true,
                  speed: 0.05,          
                },
                mode: 'x'
              }
            }
          },
          scales: {
            y: {
                beginAtZero: true
            }
          }
        },
      })
      Chart.register(zoomPlugin);
    }
  
    $('#id_calculate').on('click', function () {
      let evaluable = $('#id_function').val()
      let func_start = parseFloat($('#id_func_start').val())
      let func_end = parseFloat($('#id_func_end').val())
      let func_step = parseFloat($('#id_x_step').val())
  
      console.log(
        `Function : ${evaluable}, Function Starts At : ${func_start}, Function Ends At : ${func_end}, Step : ${func_step}`,
      )
  
      const conditions = [  // Conditions for a successful calculation
        Boolean(!evaluable),
        Boolean(func_start > func_end),
        Boolean(func_step > func_end),
        Boolean(func_step < 0),
        isNaN(func_start),
        isNaN(func_end),
        isNaN(func_step),
      ]
  
      if (conditions.includes(true)) {  // If any of the above conditions fail, form will not be submitted
        output.text('Cannot calculate the function').addClass('error')
        alert(`Cannot calculate ${evaluable}, please provide proper values!`)
      } else {
        console.log('Parse succeeded!')
        output.html('').removeClass('error') // Reset class
        let fx_values = make_fx(evaluable, func_start, func_end, func_step) // Calculates the function x and y values
  
        $.each(fx_values, function (k, value) {   // Appends the textual values of the function to the HTML output-element
          output.append(
            `<strong>${k + 1}</strong>: <i>⨍(${value.x})</i> = ${!isNaN(value.y)?value.y:" - "}<br>`,
          )
        })
  
        draw_fx(fx_values) // Draws the values to the canvas
      }
      console.log('Submit button clicked')
    })
  });
  