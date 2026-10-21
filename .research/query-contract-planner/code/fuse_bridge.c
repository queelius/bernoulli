/* Minimal ctypes bridge. Upstream binaryfusefilter.h is retained unchanged. */
#include "../vendor/binaryfusefilter.h"

typedef struct {
    uint8_t bits;
    uint64_t salt;
    union {
        binary_fuse8_t f8;
        binary_fuse16_t f16;
    } filter;
} frozen_fuse;

void fuse_free(frozen_fuse *filter) {
    if (filter == NULL) return;
    if (filter->bits == 8) binary_fuse8_free(&filter->filter.f8);
    else binary_fuse16_free(&filter->filter.f16);
    free(filter);
}

frozen_fuse *fuse_build(const uint64_t *keys, uint32_t count,
                       uint8_t bits, uint64_t salt) {
    if ((bits != 8 && bits != 16) || count < 2 || keys == NULL) return NULL;
    frozen_fuse *filter = (frozen_fuse *)calloc(1, sizeof(*filter));
    if (filter == NULL) return NULL;
    filter->bits = bits;
    filter->salt = salt;
    uint64_t *salted = (uint64_t *)malloc((size_t)count * sizeof(uint64_t));
    if (salted == NULL) {
        fuse_free(filter);
        return NULL;
    }
    for (uint32_t i = 0; i < count; ++i) salted[i] = keys[i] ^ salt;
    bool ok;
    if (bits == 8) {
        ok = binary_fuse8_allocate(count, &filter->filter.f8);
        if (ok) ok = binary_fuse8_populate(salted, count, &filter->filter.f8);
    } else {
        ok = binary_fuse16_allocate(count, &filter->filter.f16);
        if (ok) ok = binary_fuse16_populate(salted, count, &filter->filter.f16);
    }
    free(salted);
    if (!ok) {
        fuse_free(filter);
        return NULL;
    }
    return filter;
}

size_t fuse_payload_size(const frozen_fuse *filter) {
    /* Both upstream serializers write Seed and five uint32_t fields. The
     * pinned fuse16 size helper overcounts a derived SegmentLengthMask that
     * its serializer never writes; count the actual wire representation. */
    const size_t header_bytes = sizeof(uint64_t) + 5 * sizeof(uint32_t);
    return filter->bits == 8
        ? header_bytes + filter->filter.f8.ArrayLength * sizeof(uint8_t)
        : header_bytes + filter->filter.f16.ArrayLength * sizeof(uint16_t);
}

bool fuse_serialize(const frozen_fuse *filter, char *buffer, size_t length) {
    if (length != fuse_payload_size(filter)) return false;
    if (filter->bits == 8) binary_fuse8_serialize(&filter->filter.f8, buffer);
    else binary_fuse16_serialize(&filter->filter.f16, buffer);
    return true;
}

/* Upstream's unpacked deserializer trusts the caller's buffer. Check its
 * geometry and complete length before passing any external bytes to it.
 * Both supported native headers have the same fields and 28-byte wire size. */
static bool valid_payload(const char *buffer, size_t length, uint8_t bits) {
    const size_t header_bytes = sizeof(uint64_t) + 5 * sizeof(uint32_t);
    if ((bits != 8 && bits != 16) || length < header_bytes) return false;
    binary_fuse8_t geometry = {0};
    binary_fuse8_deserialize_header(&geometry, buffer);
    const uint64_t segment_length = geometry.SegmentLength;
    const uint64_t segment_count = geometry.SegmentCount;
    if (geometry.Size < 2 || segment_length == 0 || segment_length > 262144 ||
        (segment_length & (segment_length - 1)) != 0 || segment_count == 0)
        return false;
    if (segment_length * segment_count != geometry.SegmentCountLength ||
        segment_length * (segment_count + 2) != geometry.ArrayLength ||
        geometry.ArrayLength < geometry.Size)
        return false;
    const uint64_t needed = header_bytes +
        (uint64_t)geometry.ArrayLength * (bits / 8);
    return needed == length;
}

frozen_fuse *fuse_deserialize(const char *buffer, size_t length,
                             uint8_t bits, uint64_t salt) {
    if (buffer == NULL || !valid_payload(buffer, length, bits)) return NULL;
    frozen_fuse *filter = (frozen_fuse *)calloc(1, sizeof(*filter));
    if (filter == NULL) return NULL;
    filter->bits = bits;
    filter->salt = salt;
    const bool ok = bits == 8
        ? binary_fuse8_deserialize(&filter->filter.f8, buffer)
        : binary_fuse16_deserialize(&filter->filter.f16, buffer);
    if (!ok) {
        fuse_free(filter);
        return NULL;
    }
    return filter;
}

bool fuse_contains(const frozen_fuse *filter, uint64_t key) {
    const uint64_t salted = key ^ filter->salt;
    return filter->bits == 8
        ? binary_fuse8_contain(salted, &filter->filter.f8)
        : binary_fuse16_contain(salted, &filter->filter.f16);
}
