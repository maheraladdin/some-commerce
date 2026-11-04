import { appSchema, tableSchema } from '@nozbe/watermelondb';

export const commerceSchema = appSchema({
  version: 1,
  tables: [
    tableSchema({
      name: 'cart_items',
      columns: [
        { name: 'tenant_id', type: 'string', isIndexed: true },
        { name: 'product_id', type: 'string', isIndexed: true },
        { name: 'variant_id', type: 'string', isOptional: true },
        { name: 'quantity', type: 'number' },
        { name: 'unit_price_minor', type: 'number' },
        { name: 'currency', type: 'string' },
        { name: 'created_at', type: 'number' },
        { name: 'updated_at', type: 'number' },
      ],
    }),
    tableSchema({
      name: 'cached_products',
      columns: [
        { name: 'tenant_id', type: 'string', isIndexed: true },
        { name: 'title', type: 'string' },
        { name: 'slug', type: 'string', isIndexed: true },
        { name: 'price_minor', type: 'number' },
        { name: 'currency', type: 'string' },
        { name: 'etag', type: 'string' },
        { name: 'updated_at', type: 'number' },
      ],
    }),
  ],
});
