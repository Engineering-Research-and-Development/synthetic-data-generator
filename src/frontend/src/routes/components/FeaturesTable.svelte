<script lang="ts">
    import {
        Table,
        TableBody,
        TableBodyCell,
        TableBodyRow,
        TableHead,
        TableHeadCell,
        Checkbox,
    } from 'flowbite-svelte';

    type RowData = { [key: string]: any };
    type OnToggleColumn = (header: string) => void;

    let max_rows = 10; // Maximum number of rows to display
    export let headers: string[] = []; // Array of table headers
    export let tableData: RowData[] = []; // Array of table rows
    export let selectedColumns: string[] = []; // Array of selected columns
    export let onToggleColumn: OnToggleColumn; // Function to handle column toggle
</script>

<Table class="w-3/4 text-gray-500 dark:text-gray-400" shadow>
    <TableHead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        {#each headers as header}
            <TableHeadCell>
                <div class="flex items-center space-x-2">
                    <Checkbox
                            checked={selectedColumns.includes(header)}
                            on:change={() => onToggleColumn(header)}
                    />
                    <span>{header}</span>
                </div>
            </TableHeadCell>
        {/each}
    </TableHead>
    <TableBody tableBodyClass="divide-y">
        {#each tableData.slice(0, max_rows) as row}
            <TableBodyRow class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                {#each headers as header}
                    <TableBodyCell>
                        {row[header]}
                    </TableBodyCell>
                {/each}
            </TableBodyRow>
        {/each}
    </TableBody>
</Table>
