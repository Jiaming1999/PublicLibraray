/**
 * Tutorial Code from
 * @https://www.pluralsight.com/guides/drawing-charts-in-react-with-d3
 */
import * as d3 from 'd3';
import React, { useRef, useEffect } from 'react';

function BarChart({ width, height, data }) {
  const ref = useRef();

  useEffect(() => {
    const svg = d3.select(ref.current)
      .attr("width", width)
      .attr("height", height)
      .style("border", "1px solid #ececec")
  }, []);

  useEffect(() => {
    draw();
  }, [data]);

  const draw = () => {

    const svg = d3.select(ref.current);
    var selection = svg.selectAll("rect").data(data);
    var yScale = d3.scaleLinear()
      .domain([0, d3.max(data)])
      .range([0, height - 100]);

    svg
      .append("text")
      .text(d => d)

    selection
      .transition().duration(300)
      .attr("height", (d) => yScale(d))
      .attr("y", (d) => height - yScale(d))

    selection
      .enter()
      .append("rect")
      .attr("x", (d, i) => i * 5 + 'vw')
      .attr("y", (d) => height)
      .attr("width", "3vw")
      .attr("height", 10)
      .attr("fill", "#3448a8")
      .transition().duration(300)
      .attr("height", (d) => yScale(d))
      .attr("y", (d) => height - yScale(d))

    selection
      .exit()
      .transition().duration(300)
      .attr("y", (d) => height)
      .attr("height", 0)
      .remove()
  }


  return (
    <div className="chart">
      <svg ref={ref}>
      </svg>
    </div>
  )

}

export default BarChart;