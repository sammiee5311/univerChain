from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(verbose_name="Category Name", help_text="Required and unique", max_length=255, unique=True)
    slug = models.SlugField(verbose_name="Category URL", max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(verbose_name="Product Name", help_text="Required", max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Product Type"
        verbose_name_plural = "Product Types"

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name="Name", help_text="Required", max_length=255)

    class Meta:
        verbose_name = "Product Specification"
        verbose_name_plural = "Product Specifications"

    def __str__(self):
        return self.name


class Product(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    title = models.CharField(verbose_name="title", help_text="Required", max_length=255)
    description = models.TextField(verbose_name="description", help_text="Not Required", blank=True)
    slug = models.SlugField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField("created at", auto_now_add=True, editable=False)
    updated_at = models.DateTimeField("updated at", auto_now=True)
    regular_price = models.DecimalField(
        verbose_name="Regular Price",
        help_text="Maximum 100.00",
        error_messages={"name": {"max_length": "The price must be between 0 and 100.00"}},
        max_digits=5,
        decimal_places=1,
    )
    discount_price = models.DecimalField(
        verbose_name="Discount Price",
        help_text="Maximum 100.00",
        error_messages={"name": {"max_length": "The price must be between 0 and 100.00"}},
        max_digits=5,
        decimal_places=1,
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ("-created_at",)

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])

    def __str__(self):
        return self.title


class ProductSpecificationValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(verbose_name="value", max_length=255)

    class Meta:
        verbose_name = "Product Specification Value"
        verbose_name_plural = "Product Specification Values"

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(
        verbose_name="image", help_text="Upload a product image", upload_to="images/", default="images/default.png"
    )
    alt_info = models.CharField(
        verbose_name="Alternative Information",
        help_text="Please write Alternative Information",
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateField("created at", auto_now_add=True, editable=False)
    updated_at = models.DateTimeField("updated at", auto_now=True)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
