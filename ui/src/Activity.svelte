<script>
    export let data;
    export let index;
</script>

<table>
    <thead>
        <tr>
            <th>Key</th>
            <th>Value</th>
        </tr>
    </thead>
    <tbody>
        {#if !index}
            No Selection...
        {:else}
            {#each data.columns as col, i}
                <tr>
                    <td>
                        {col}
                    </td>
                    <td>
                        {data.data[data.index[index]][i]}
                    </td>
                </tr>
            {/each}
        {/if}
    </tbody>
</table>
