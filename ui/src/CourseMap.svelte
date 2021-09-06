<script>
    import { onMount } from "svelte";

    export let course;

    let mapLoaded = false;
    let config = { responsive: true };

    const graphID = "courseMap";

    $: lat_lon = course.ok ? [course["lat"][0], course["lon"][0]] : [0, 0];
    $: layout = {
        title: "Course Map",
        dragmode: "zoom",
        mapbox: {
            style: "open-street-map",
            center: { lat: lat_lon[0], lon: lat_lon[1] },
            zoom: 11,
        },
        margin: { r: 0, t: 0, b: 0, l: 0 },
    };
    $: data = course.ok
        ? [
              {
                  lat: Object.values(course["lat"]),
                  lon: Object.values(course["lon"]),
                  type: "scattermapbox",
              },
          ]
        : [{ type: "scattermapbox" }];

    $: {
        if (mapLoaded) {
            Plotly.react(graphID, data, layout);
        }
    }

    onMount(() => {
        Plotly.newPlot(graphID, data, layout, config);
        mapLoaded = true;
    });
</script>

{#if !course.ok}
    <span>{course.message}</span>
{/if}
<div id="courseMap" />

<!-- {#if course.ok}
        <code>{JSON.stringify(data)}</code>
    {/if} -->
<style>
    span {
        background-color: lightcoral;
        padding: 5px;
    }

    #courseMap {
        height: 100%;
        width: 100%;
    }

    /* #courseMap {
        
    } */

    /* .hidden {
        display: none;
    } */
</style>
