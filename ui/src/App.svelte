<script>
    import { onMount } from "svelte";
    import Activity from "./Activity.svelte";
    import CourseMap from "./CourseMap.svelte";
import LineGraph from "./LineGraph.svelte";
    import Table from "./Table.svelte";

    export let api;

    let activities;

    onMount(async () => {
        const res = await fetch(api + "activities");
        activities = await res.json();
    });

    $: indices = activities
        ? [
              "Activity ID",
              "Activity Date",
              "Activity Name",
              "Activity Type",
              "Elapsed Time",
              "Distance",
          ].map((e) => activities.columns.findIndex((a) => a == e))
        : [];

    let selectedActivity;
    let selectedActivityCourse = { ok: false, message: "no selection" };

    async function getCourse(id) {
        const res = await fetch(api + `activities/${id}`);
        // console.log(res);
        if (res.status != 200) {
            selectedActivityCourse = { ok: false, message: await res.text() };
            return;
        }
        let json = await res.json();
        json["ok"] = true;
        selectedActivityCourse = json;
    }

    function activitySelected(event) {
        selectedActivity = event.detail.index;
        getCourse(activities.data[activities.index[selectedActivity]][0]);
    }


    $: time = selectedActivityCourse.ok ? Object.values(selectedActivityCourse['time']).map(v => new Date(v)) : [];
    $: speed = selectedActivityCourse.ok && selectedActivityCourse['speed'] ? Object.values(selectedActivityCourse['speed']) : [];
</script>

<main>
    {#if !activities}
        Loading...
    {:else}
        <div class="activities_table">
            <Table {indices} data={activities} on:selected={activitySelected} />
        </div>
        <div class="plot" id='kinematics_plot'>
            <LineGraph x={time} y={speed}/>
        </div>
        <div class="activity_info">
            <Activity data={activities} index={selectedActivity} />
        </div>
        <div class="activity_course">
            <CourseMap course={selectedActivityCourse} />
        </div>
    {/if}
</main>

<style>
    :global(body) {
        /* this will apply to <body> */
        margin: 0;
        padding: 0;
    }
    main {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        grid-template-rows: 2fr 2fr;
        height: 100vh;
    }
    .activities_table {
        overflow: auto;
        grid-column: 1 / span 2;
        grid-row: 1;
    }

    .activity_info {
        overflow: auto;
        grid-column: 1;
        grid-row: 2;
    }

    .activity_course {
        overflow: auto;
        grid-column: 2 / span 2;
        grid-row: 2;
    }

    #kinematics_plot {
        grid-row: 1;
        grid-column: 3;
    }
</style>
