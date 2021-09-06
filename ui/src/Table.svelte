<script>
    import { createEventDispatcher } from "svelte";

    export let indices;
    export let data;

    let selected;

    const dispatch = createEventDispatcher();

    function rowClicked(i) {
        return (event) => {
            dispatch("selected", {
                index: i,
            });
        };
    }
</script>

<table>
    <thead>
        <tr>
            <th><span class="text">Index</span></th>
            {#each indices as i}
                <th><span class="text">{data.columns[i]}</span></th>
            {/each}
        </tr>
    </thead>
    <tbody>
        {#each data.index as i}
            <tr on:click={rowClicked(i)}>
                <th>{i}</th>
                {#each indices as ii}
                    <td>{data.data[i][ii]}</td>
                {/each}
            </tr>
        {/each}
    </tbody>
</table>

<style>
    table {
        height: 100%;
        overflow: scroll;
        /* margin-top:20px; */
    }
    tbody tr {
        cursor: pointer;
    }
    tr:nth-child(2n) {
        background-color: lightgray;
    }
</style>
